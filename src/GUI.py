import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import cairo

import sys

class MainWindow:

	def __init__(self):
		self.builder = None
		self.object_list = None
		self.object_id = 0
		self.object_list = None

	def run(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("../ui/GUI.glade")
		self.window = self.builder.get_object("main_window")
		self.object_list = self.builder.get_object("liststore1")


		self.builder.connect_signals(MainWindowHandler(self))
		self.window.show_all()

		Gtk.main()

class MainWindowHandler:

	def __init__(self, main_window):
		self.builder = main_window.builder
		self.main_window = main_window
		self.object_list = main_window.object_list

		self.object_id = main_window.object_id

	def new_object_button_clicked_cb(self, widget):
		self.builder.add_from_file("../ui/new_object.glade")
		self.object_window = self.builder.get_object("window_new_object")
		self.builder.connect_signals(NewObjectHandler(self, self.object_window))

		self.object_window.show_all()

	def on_main_window_destroy(self, object, data=None):
		print("quit")
		Gtk.main_quit()


class NewObjectHandler:

	def __init__(self, main_window, object_window):
		self.main_window = main_window
		self.builder = main_window.builder
		self.object_window = object_window

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

			print(x, y)


		self.main_window.object_list.append([object_id, object_name, "Point"])
		self.object_window.destroy()