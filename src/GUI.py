import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import cairo

import sys

class MainWindow:

	def __init__(self):
		self.builder = None
		self.object_list = None

	def run(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("../ui/GUI.glade")
		self.builder.connect_signals(MainWindowHandler(self))
		self.window = self.builder.get_object("main_window")
		self.object_list = self.builder.get_object("object_scrolled_window")
		self.window.show_all()

		Gtk.main()

class MainWindowHandler:

	def __init__(self, main_window):
		self.builder = main_window.builder

	def new_object_button_clicked_cb(self, widget):
		self.builder.add_from_file("../ui/new_object.glade")
		self.obj_window = self.builder.get_object("window_new_object")
		self.obj_window.show_all()

	def on_main_window_destroy(self, object, data=None):
		print("quit")
		Gtk.main_quit()
