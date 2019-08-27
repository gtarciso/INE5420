import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import cairo

import objects
import window
import viewport

import numpy as np

import sys

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


	def run(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("../ui/GUI.glade")
		self.window = self.builder.get_object("main_window")
		self.object_list = self.builder.get_object("liststore1")
		self.darea = self.builder.get_object("viewport")

		#xvp = self.darea.get_allocation().width
		#yvp = self.darea.get_allocation().height

		#(xvp, yvp) = self.darea.size_request()

		self.vp_window = window.Window(0, 0, 100, 100)
		self.viewport = viewport.Viewport(0, 550, 0, 500, self.vp_window)

		self.builder.connect_signals(MainWindowHandler(self))
		self.window.show_all()

		Gtk.main()

class MainWindowHandler:

	def __init__(self, main_window):
		self.builder = main_window.builder
		self.main_window = main_window
		self.object_list = main_window.object_list
		self.darea = main_window.darea
		self.saved_objects = main_window.saved_objects
		self.viewport = main_window.viewport
		self.window = main_window.vp_window

		self.object_id = main_window.object_id

	def new_object_button_clicked_cb(self, widget):
		self.builder.add_from_file("../ui/new_object.glade")
		self.object_window = self.builder.get_object("window_new_object")
		self.builder.connect_signals(NewObjectHandler(self, self.object_window))

		self.object_window.show_all()


	def delete_object_button_clicked_cb(self, widget):
		print("delete")
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()

		for val in path:
			it = model.get_iter(path)
			object_id = int(model.get_value(it, 0))

			for i in range(len(self.saved_objects)):
				if self.saved_objects[i].object_id == object_id:
					self.saved_objects.pop(i)
					break

			model.remove(it)

		self.darea.queue_draw()

	def clear_object_button_clicked_cb(self, widget):
		tree_view = self.builder.get_object("list_obj_created")
		(model, path) = tree_view.get_selection().get_selected_rows()
		model.clear()
		self.saved_objects.clear()

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
					break

		self.saved_objects[obj_id].scale(step_entry, step_entry)
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
					break

		self.saved_objects[obj_id].scale(1/step_entry, 1/step_entry)
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

		self.saved_objects[obj_id].rotate(theta)

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
					break


		self.saved_objects[obj_id].traverse(0, step_entry)

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
					break


		self.saved_objects[obj_id].traverse(-step_entry, 0)

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
					break

		self.saved_objects[obj_id].traverse(step_entry, 0)

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
					break

		
		self.saved_objects[obj_id].traverse(0, -step_entry)

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


# teste, alterar para desenhar objetos
	def on_viewport_draw(self, widget, cr):
		x_max = self.main_window.darea.get_allocation().width
		y_max = self.main_window.darea.get_allocation().height


		cr.save()
		cr.set_source_rgb(0, 0, 0)
		cr.move_to(0, 0)
		cr.line_to(0, y_max)
		cr.line_to(x_max, y_max)
		cr.line_to(x_max, 0)
		cr.line_to(0, 0)
		cr.fill()
		cr.restore()

		for obj in self.main_window.saved_objects:
			if obj.object_type == "Point":
				obj.draw_point(cr, self.viewport)

			elif obj.object_type == "Line":
				obj.draw_line(cr, self.viewport)

			elif obj.object_type == "Wireframe":
				obj.draw_wireframe(cr, self.viewport)



class NewObjectHandler:

	def __init__(self, main_window, object_window):
		self.main_window = main_window
		self.builder = main_window.builder
		self.object_window = object_window
		self.darea = main_window.darea
		self.wireframe_points = []


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
		self.main_window.object_id += 1
		object_id = self.main_window.object_id
		print(self.main_window.object_id)
		current_page = self.builder.get_object("notebook_object").get_current_page()
		print(current_page)


		# if current page = 0, add point
		if current_page == 0:
			x = float(self.builder.get_object("entry_x_point").get_text())
			y = float(self.builder.get_object("entry_y_point").get_text())

			new_point = objects.Point(x, y, object_id, object_name, "Point")
			self.main_window.object_list.append([new_point.object_id, new_point.object_name, new_point.object_type])


			self.main_window.saved_objects.append(new_point)


		if current_page == 1:
			x1 = float(self.builder.get_object("entry_x1_line").get_text())
			x2 = float(self.builder.get_object("entry_x2_line").get_text())
			y1 = float(self.builder.get_object("entry_y1_line").get_text())
			y2 = float(self.builder.get_object("entry_y2_line").get_text())

			new_line = objects.Line(objects.LinePoint(x1, y1), objects.LinePoint(x2, y2), object_id, object_name, "Line")
			self.main_window.object_list.append([new_line.object_id, new_line.object_name, new_line.object_type])
			self.main_window.saved_objects.append(new_line)

		if current_page == 2:

			new_list = []

			for obj in self.wireframe_points:
				new_list.append(obj)

			new_wireframe = objects.Wireframe(new_list, object_id, object_name, "Wireframe")
			self.main_window.object_list.append([new_wireframe.object_id, new_wireframe.object_name, new_wireframe.object_type])
			self.main_window.saved_objects.append(new_wireframe)

			self.wireframe_points.clear()


		cr = self.darea.get_window().cairo_create()
		self.darea.draw(cr)

		self.object_window.destroy()

	def button_add_wireframe_point_clicked_cb(self, widget):
		print("adding point")

		x = float(self.builder.get_object("entry_x_wireframe").get_text())
		y = float(self.builder.get_object("entry_y_wireframe").get_text())
		new_point = objects.LinePoint(x, y)

		self.wireframe_points.append(new_point)