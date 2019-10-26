import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import cairo
from gi.repository import GObject

import objects
import window
import viewport
import descriptorOBJ

#import gtk

import numpy as np

import sys

class RotationType:
	CENTER_OBJECT = 1
	CENTER_WORLD = 2
	ARBITRARY = 3

class MainWindow:

	def __init__(self):
		self.builder = None
		self.object_list = None
		self.object_id = 0
		self.darea = None
		self.saved_objects = []
		self.window = None
		self.viewport = None
		self.vp_window = None
		self.available_id = []
		self.log = None


	def run(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("../ui/GUI.glade")
		self.window = self.builder.get_object("main_window")
		self.object_list = self.builder.get_object("liststore1")
		self.darea = self.builder.get_object("viewport")
		self.log = self.builder.get_object("textview_log")

		#xvp = self.darea.get_allocation().width
		#yvp = self.darea.get_allocation().height

		#(xvp, yvp) = self.darea.size_request()

		self.vp_window = window.Window(0, 0, 100, 100)
		self.viewport = viewport.Viewport(20, 530, 20, 480, self.vp_window)

		self.builder.connect_signals(MainWindowHandler(self))
		self.window.show_all()

		Gtk.main()

	def append_log(self, text):
		log_buffer = self.log.get_buffer()
		it = log_buffer.get_iter_at_offset(-1)
		log_buffer.insert(it, text + "\n", -1)

class MainWindowHandler:

	def __init__(self, main_window):
		self.builder = main_window.builder
		self.main_window = main_window
		self.object_list = main_window.object_list
		self.darea = main_window.darea
		self.saved_objects = main_window.saved_objects
		self.viewport = main_window.viewport
		self.window = main_window.vp_window
		self.available_id = main_window.available_id
		self.log = main_window.log

		# 
		self.rotate_type = RotationType.CENTER_OBJECT

		self.object_id = main_window.object_id

	def reset_window_button_clicked_cb(self, widget):
		self.window.reset(0, 0, 100, 100)
		for obj in self.main_window.saved_objects:
			obj.reset_scn()


		self.darea.queue_draw()

	def new_object_button_clicked_cb(self, widget):
		self.builder.add_from_file("../ui/new_object.glade")
		self.object_window = self.builder.get_object("window_new_object")
		self.builder.connect_signals(NewObjectHandler(self, self.object_window))

		self.object_window.show_all()


	def load_object_button_clicked_cb(self, widget):
		self.dlg = Gtk.FileChooserDialog(None, None, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		self.response = self.dlg.run()
		file_name = self.dlg.get_filename()
		if self.response == Gtk.ResponseType.OK:
			self.main_window.append_log("From file " + file_name + " loaded the objects:")


		if self.response == Gtk.ResponseType.CANCEL:
			self.main_window.append_log("Failed to load from file")

		self.dlg.destroy()
		self.object_id += 1
		(objects, window_atr) = descriptorOBJ.objectDescriptor.load_file(file_name, self.object_id)
		self.window.set_atributes(window_atr[0], window_atr[1], window_atr[2], window_atr[3])
		for obj in objects:
			obj_id = int(obj.object_id)
			obj_name = str(obj.object_name)
			obj_type = str(obj.object_type)
			self.main_window.append_log("Object " + obj_name + " loaded")
			self.object_list.append([obj_id, obj_name, obj_type])
			self.saved_objects.append(obj)


		#self.text.set_text(dlg.get_filename())


	def delete_object_button_clicked_cb(self, widget):
		print("delete")
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()
		old_obj_id = -1

		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))
			old_obj_id = int(object_id)
			obj_name = str(model.get_value(it, 1))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id and self.saved_objects[i].object_name == obj_name:
					self.main_window.append_log("Object " + self.saved_objects[i].object_name + 
						" (" + self.saved_objects[i].object_type + ") deleted")
					self.saved_objects.pop(i)
					break

			model.remove(it)


		flag_found = 0

		for i in range(len(self.saved_objects)):
			if self.saved_objects[i].object_id == old_obj_id:
				flag_found = 1

		if flag_found == 0:
			self.available_id.append(old_obj_id)

		

		self.darea.queue_draw()

	def clear_object_button_clicked_cb(self, widget):
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()
		model.clear()

		for i in range(len(self.saved_objects)):
			self.available_id.append(self.saved_objects[i].object_id)

		self.saved_objects.clear()
		self.main_window.append_log("All objects deleted")

		self.darea.queue_draw()

	# zoom in button
	def in_button_clicked_cb(self, widget):
		step_entry = float(self.builder.get_object("step_entry").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					if self.saved_objects[obj_id].object_type == "3D Object":
						self.saved_objects[obj_id].scale(step_entry, step_entry, step_entry)
					else:
						self.saved_objects[obj_id].scale(step_entry, step_entry)
					
					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)


		self.darea.queue_draw()

	def out_button_clicked_cb(self, widget):
		step_entry = float(self.builder.get_object("step_entry").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					if self.saved_objects[obj_id].object_type == "3D Object":
						self.saved_objects[obj_id].scale(1/step_entry, 1/step_entry, 1/step_entry)
					else:
						self.saved_objects[obj_id].scale(1/step_entry, 1/step_entry)
					
					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)

		self.darea.queue_draw()


	def x_rotate_3d_clicked_cb(self, widget):

		angle_entry = float(self.builder.get_object("angle_entry_3d").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		theta = (angle_entry/180)*np.pi
		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					self.saved_objects[obj_id].rotate_x(theta)
					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)

		self.main_window.append_log("Object rotated around x-axis")

		self.darea.queue_draw()


	def y_rotate_3d_clicked_cb(self, widget):
		angle_entry = float(self.builder.get_object("angle_entry_3d").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		theta = (angle_entry/180)*np.pi
		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					self.saved_objects[obj_id].rotate_y(theta)
					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)

		self.main_window.append_log("Object rotated around y-axis")
		self.darea.queue_draw()


	def z_rotate_3d_clicked_cb(self, widget):
		angle_entry = float(self.builder.get_object("angle_entry_3d").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		theta = (angle_entry/180)*np.pi
		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					self.saved_objects[obj_id].rotate_z(theta)
					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)

		
		self.main_window.append_log("Object rotated around z-axis")
		self.darea.queue_draw()



	def arbitrary_axis_rotate_clicked_cb(self, widget):
		x0 = float(self.builder.get_object("x0_entry").get_text())
		xf = float(self.builder.get_object("xf_entry").get_text())
		y0 = float(self.builder.get_object("y0_entry").get_text())
		yf = float(self.builder.get_object("yf_entry").get_text())
		z0 = float(self.builder.get_object("z0_entry").get_text())
		zf = float(self.builder.get_object("zf_entry").get_text())

		angle = float(self.builder.get_object("arbitrary_axis_entry").get_text())
		theta = (angle/180)*np.pi

		delta_x = xf - x0
		delta_y = yf - y0
		delta_z = zf - z0

		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					self.saved_objects[obj_id].rotateArbitraryAxis(theta, delta_x, delta_y, delta_z)
					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)

		
		self.main_window.append_log("Object rotated around arbitrary axis")
		self.darea.queue_draw()

	def rotate_button_clicked_cb(self, widget):

		angle_entry = float(self.builder.get_object("angle_entry").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					break

		theta = (angle_entry/180)*np.pi

		if self.rotate_type == RotationType.CENTER_OBJECT:
			self.saved_objects[obj_id].rotate(theta)
			self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)

		elif self.rotate_type == RotationType.CENTER_WORLD:
			cx = (self.window.x_max - self.window.x_min)/2
			cy = (self.window.y_max - self.window.y_min)/2
			self.saved_objects[obj_id].rotateArbitraryPoint(theta, cx, cy)
			self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)

		elif self.rotate_type == RotationType.ARBITRARY:
			x_point = float(self.builder.get_object("x_rotate_entry").get_text())
			y_point = float(self.builder.get_object("y_rotate_entry").get_text())
			self.saved_objects[obj_id].rotateArbitraryPoint(theta, x_point, y_point)
			self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)

		self.darea.queue_draw()



	def z_in_button_clicked_cb(self, widget):
		step_entry = float(self.builder.get_object("step_entry").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					self.saved_objects[obj_id].traverse(0, 0, step_entry)
					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)

		self.darea.queue_draw()


	def z_out_button_clicked_cb(self, widget):
		step_entry = float(self.builder.get_object("step_entry").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					self.saved_objects[obj_id].traverse(0, 0, -step_entry)
					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)

		self.darea.queue_draw()
					

	def up_button_clicked_cb(self, widget):
		step_entry = float(self.builder.get_object("step_entry").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					if self.saved_objects[obj_id].object_type == "3D Object":
						self.saved_objects[obj_id].traverse(0, step_entry, 0)
					else:
						self.saved_objects[obj_id].traverse(0, step_entry)

					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)
						

		self.darea.queue_draw()

	def left_button_clicked_cb(self, widget):
		step_entry = float(self.builder.get_object("step_entry").get_text())

		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					if self.saved_objects[obj_id].object_type == "3D Object":
						self.saved_objects[obj_id].traverse(-step_entry, 0, 0)
					else:
						self.saved_objects[obj_id].traverse(-step_entry, 0)

					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)


		self.darea.queue_draw()

	def right_button_clicked_cb(self, widget):
		step_entry = float(self.builder.get_object("step_entry").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					if self.saved_objects[obj_id].object_type == "3D Object":
						self.saved_objects[obj_id].traverse(step_entry, 0, 0)
					else:
						self.saved_objects[obj_id].traverse(step_entry, 0)

					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)
		

		self.darea.queue_draw()

	def down_button_clicked_cb(self, widget):
		step_entry = float(self.builder.get_object("step_entry").get_text())
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		obj_id = -1
		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					obj_id = i
					if self.saved_objects[obj_id].object_type == "3D Object":
						self.saved_objects[obj_id].traverse(0, -step_entry, 0)
					else:
						self.saved_objects[obj_id].traverse(0, -step_entry)

					self.saved_objects[obj_id].rotate_scn(-self.window.theta, self.window.window_center.x, self.window.window_center.y)
		

		self.darea.queue_draw()


	def rotate_window_button_clicked_cb(self, widget):
		angle_entry = float(self.builder.get_object("window_angle_entry").get_text())
		self.window.rotate(angle_entry)
		win_theta = (-self.window.theta/180)*np.pi
		for obj in self.main_window.saved_objects:
			obj.rotate_scn(win_theta, self.window.window_center.x, self.window.window_center.y)

		self.darea.queue_draw()

	def button_window_up_clicked_cb(self, widget):
		self.window.move_up()
		self.darea.queue_draw()

	def button_window_down_clicked_cb(self, widget):
		self.window.move_down()
		self.darea.queue_draw()

	def button_window_left_clicked_cb(self, widget):
		self.window.move_left()
		self.darea.queue_draw()

	def button_window_right_clicked_cb(self, widget):
		self.window.move_right()
		self.darea.queue_draw()

	def zoom_in_button_clicked_cb(self, widget):
		self.window.zoom_in()
		self.darea.queue_draw()

	def zoom_out_button_clicked_cb(self, widget):
		self.window.zoom_out()
		self.darea.queue_draw()

	def on_main_window_destroy(self, object, data=None):
		print("quit")
		Gtk.main_quit()

	def on_rb_centro_objeto_toggled(self, widget):
		self.rotate_type = RotationType.CENTER_OBJECT


	def on_rb_centro_mundo_toggled(self, widget):
		self.rotate_type = RotationType.CENTER_WORLD


	def on_rb_ponto_arbitrario_toggled(self, widget):
		self.rotate_type = RotationType.ARBITRARY

	def perspective_clicked_cb(self, widget):
		self.darea.queue_draw()


# teste, alterar para desenhar objetos
	def on_viewport_draw(self, widget, cr):
		x_max = self.main_window.darea.get_allocation().width
		y_max = self.main_window.darea.get_allocation().height

		pr = self.builder.get_object("perspective")


		cr.save()
		cr.set_source_rgb(0, 0, 0)
		cr.move_to(0, 0)
		cr.line_to(0, y_max)
		cr.line_to(x_max, y_max)
		cr.line_to(x_max, 0)
		cr.line_to(0, 0)
		cr.fill()
		cr.set_source_rgb(1, 1, 1)
		cr.move_to(self.viewport.x_min, self.viewport.y_min)
		cr.line_to(self.viewport.x_min, self.viewport.y_max)
		cr.line_to(self.viewport.x_max, self.viewport.y_max)
		cr.line_to(self.viewport.x_max, self.viewport.y_min)
		cr.line_to(self.viewport.x_min, self.viewport.y_min)
		cr.stroke()
		cr.restore()

		win_theta = (-self.window.theta/180)*np.pi

		for obj in self.main_window.saved_objects:
			if obj.object_type == "Point":
				obj.rotate_scn(win_theta, self.window.window_center.x, self.window.window_center.y)
				obj.clip_point(self.window)
				if obj.visible:
					obj.draw_point(cr, self.viewport)

			elif obj.object_type == "Line":
				obj.rotate_scn(win_theta, self.window.window_center.x, self.window.window_center.y)
				obj.clip_line(self.window)
				if obj.visible:
					obj.draw_line(cr, self.viewport)

			elif obj.object_type == "Wireframe":
				obj.rotate_scn(win_theta, self.window.window_center.x, self.window.window_center.y)
				obj.clip_wireframe(self.window)

				obj.draw_wireframe(cr, self.viewport)

			elif obj.object_type == "Curve":
				obj.rotate_scn(win_theta, self.window.window_center.x, self.window.window_center.y)
				obj.clip_curve(self.window)

				obj.draw_curve(cr, self.viewport)

			elif obj.object_type == "3D Object":
				obj.rotate_scn(win_theta, self.window.window_center.x, self.window.window_center.y)
				if pr.get_active():
					obj.project(0.5)
				obj.clip_object(self.window)
				obj.draw_object(cr, self.viewport)

	def append_log(self, text):
		log_buffer = self.log.get_buffer()
		it = log_buffer.get_iter_at_offset(-1)
		log_buffer.insert(it, text + "\n", -1)





class NewObjectHandler:

	def __init__(self, main_window, object_window):
		self.main_window = main_window
		self.builder = main_window.builder
		self.object_window = object_window
		self.darea = main_window.darea
		self.wireframe_points = []
		self.bspline_points = []


	def on_window_new_object_destroy(self, object, data=None):				
		print("new object window closed")
		self.object_window.destroy()

	def on_cancel_button_clicked(self, widget):
		print("action canceled")
		self.object_window.destroy()

	def on_ok_button_clicked(self, widget):
		print("clicked")

		object_name = self.builder.get_object("entry_name").get_text()
		print(object_name)
		if len(self.main_window.available_id) == 0:
			self.main_window.object_id += 1
			object_id = self.main_window.object_id
		elif len(self.main_window.available_id) != 0:
			object_id = self.main_window.available_id[0]
			self.main_window.available_id.pop(0)

		if object_name == "":
			object_name = "object"+str(object_id)
			print(object_id)
		current_page = self.builder.get_object("notebook_object").get_current_page()

		color = self.builder.get_object("color_button")
		rgba = color.get_rgba()

		object_rgb = []
		object_rgb.append(rgba.red)
		object_rgb.append(rgba.green)
		object_rgb.append(rgba.blue)

		is_solid = self.builder.get_object("button_solid")

		# if current page = 0, add point
		if current_page == 0:
			x = float(self.builder.get_object("entry_x_point").get_text())
			y = float(self.builder.get_object("entry_y_point").get_text())

			new_point = objects.Point(x, y, object_id, object_name, "Point", object_rgb)
			new_point.rotate_scn(-self.main_window.window.theta, self.main_window.window.window_center.x, self.main_window.window.window_center.y)
			self.main_window.object_list.append([new_point.object_id, new_point.object_name, new_point.object_type])
			self.main_window.append_log("Object " + new_point.object_name + " (" + new_point.object_type + ") created")

			self.main_window.saved_objects.append(new_point)


		if current_page == 1:
			x1 = float(self.builder.get_object("entry_x1_line").get_text())
			x2 = float(self.builder.get_object("entry_x2_line").get_text())
			y1 = float(self.builder.get_object("entry_y1_line").get_text())
			y2 = float(self.builder.get_object("entry_y2_line").get_text())

			new_line = objects.Line(objects.LinePoint(x1, y1), objects.LinePoint(x2, y2), object_id, object_name, "Line", object_rgb)
			new_line.rotate_scn(-self.main_window.window.theta, self.main_window.window.window_center.x, self.main_window.window.window_center.y)
			self.main_window.object_list.append([new_line.object_id, new_line.object_name, new_line.object_type])
			self.main_window.append_log("Object " + new_line.object_name + " (" + new_line.object_type + ") created")

			self.main_window.saved_objects.append(new_line)

		if current_page == 2:

			new_list = []

			for obj in self.wireframe_points:
				new_list.append(obj)

			new_wireframe = objects.Wireframe(new_list, object_id, object_name, "Wireframe", object_rgb, is_solid.get_active())
			new_wireframe.rotate_scn(-self.main_window.window.theta, self.main_window.window.window_center.x, self.main_window.window.window_center.y)

			self.main_window.object_list.append([new_wireframe.object_id, new_wireframe.object_name, new_wireframe.object_type])
			self.main_window.append_log("Object " + new_wireframe.object_name + " (" + new_wireframe.object_type + ") created")
			self.main_window.saved_objects.append(new_wireframe)

			self.wireframe_points.clear()


		if current_page == 3:
			x1 = float(self.builder.get_object("x1_bezier_entry").get_text())
			x2 = float(self.builder.get_object("x2_bezier_entry").get_text())
			x3 = float(self.builder.get_object("x3_bezier_entry").get_text())
			x4 = float(self.builder.get_object("x4_bezier_entry").get_text())
			y1 = float(self.builder.get_object("y1_bezier_entry").get_text())
			y2 = float(self.builder.get_object("y2_bezier_entry").get_text())
			y3 = float(self.builder.get_object("y3_bezier_entry").get_text())
			y4 = float(self.builder.get_object("y4_bezier_entry").get_text())

			points = []

			points.append(objects.LinePoint(x1, y1))
			points.append(objects.LinePoint(x2, y2))
			points.append(objects.LinePoint(x3, y3))
			points.append(objects.LinePoint(x4, y4))

			new_curve = objects.Curve(points, object_id, object_name, "Curve", object_rgb, "bezier")
			new_curve.rotate_scn(-self.main_window.window.theta, self.main_window.window.window_center.x, self.main_window.window.window_center.y)
			self.main_window.object_list.append([new_curve.object_id, new_curve.object_name, new_curve.object_type])
			self.main_window.append_log("Object " + new_curve.object_name + " (Bezier " + new_curve.object_type + ") created")
			self.main_window.saved_objects.append(new_curve)

		if current_page == 4:
			if len(self.bspline_points) >= 4:
				new_list = []

				for obj in self.bspline_points:
					new_list.append(obj)

				new_bspline = objects.Curve(new_list, object_id, object_name, "Curve", object_rgb, "b-spline")
				new_bspline.rotate_scn(-self.main_window.window.theta, self.main_window.window.window_center.x, self.main_window.window.window_center.y)
				self.main_window.object_list.append([new_bspline.object_id, new_bspline.object_name, new_bspline.object_type])
				self.main_window.append_log("Object " + new_bspline.object_name + " (B-Spline " + new_bspline.object_type + ") created")
				self.main_window.saved_objects.append(new_bspline)
			else:
				self.errordialog = self.builder.get_object("bspline_error")
				self.errordialog.run()
				self.errordialog.destroy()
				self.main_window.append_log("Insufficient points to generate a b-spline curve")
				self.main_window.append_log("Try again with at least 4 points")


		self.wireframe_points.clear()
		self.bspline_points.clear()

		cr = self.darea.get_window().cairo_create()
		self.darea.draw(cr)

		self.object_window.destroy()

	def button_add_wireframe_point_clicked_cb(self, widget):

		x = float(self.builder.get_object("entry_x_wireframe").get_text())
		y = float(self.builder.get_object("entry_y_wireframe").get_text())
		self.main_window.append_log("Point (" + str(x) + ", " + str(y) + ") added to the wireframe")
		new_point = objects.LinePoint(x, y)

		self.wireframe_points.append(new_point)


	def button_add_curve_point_clicked_cb(self, widget):

		x = float(self.builder.get_object("entry_x_curve").get_text())
		y = float(self.builder.get_object("entry_y_curve").get_text())
		self.main_window.append_log("Point (" + str(x) + ", " + str(y) + ") added to the b-spline curve")

		new_point = objects.LinePoint(x, y)
		self.bspline_points.append(new_point)



