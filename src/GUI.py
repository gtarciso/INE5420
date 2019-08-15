import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import cairo

import objects

import sys

class MainWindow:

	def __init__(self):
		self.builder = None
		self.object_list = None
		self.object_id = 0
		self.darea = None
		self.saved_objects = []


	def run(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("../ui/GUI.glade")
		self.window = self.builder.get_object("main_window")
		self.object_list = self.builder.get_object("liststore1")
		self.darea = self.builder.get_object("viewport")


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

		self.object_id = main_window.object_id

	def new_object_button_clicked_cb(self, widget):
		self.builder.add_from_file("../ui/new_object.glade")
		self.object_window = self.builder.get_object("window_new_object")
		self.builder.connect_signals(NewObjectHandler(self, self.object_window))

		self.object_window.show_all()
		

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
				obj.draw_point(cr)

			elif obj.object_type == "Line":
				obj.draw_line(cr)





class NewObjectHandler:

	def __init__(self, main_window, object_window):
		self.main_window = main_window
		self.builder = main_window.builder
		self.object_window = object_window
		self.darea = main_window.darea


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


		cr = self.darea.get_window().cairo_create()
		self.darea.draw(cr)

		self.object_window.destroy()