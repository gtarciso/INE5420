import GUI
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import cairo

import sys


app = GUI.MainWindow()
exit_status = app.run()
sys.exit(exit_status)