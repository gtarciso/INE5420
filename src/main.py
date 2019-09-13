import GUI
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import cairo

import sys

print("Trabalho da disciplina INE5420 - Computação Gráfica")
print("Feito pelos alunos:")
print("Gustavo Tarciso da Silva - 14100833")
print("Mathias Olivio Reolon - 14100860")

app = GUI.MainWindow()
exit_status = app.run()
sys.exit(exit_status)