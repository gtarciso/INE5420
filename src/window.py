#from objects import MatrixTransform

class Window:

	def __init__(self, xmin, ymin, xmax, ymax):
		self.x_min = xmin
		self.x_max = xmax
		self.y_min = ymin
		self.y_max = ymax
		#self.tr_matrix = MatrixTransform()

	def move_up(self):
		self.y_min += 5
		self.y_max += 5

	def move_down(self):
		self.y_min -= 5
		self.y_max -= 5

	def move_left(self):
		self.x_min -= 5
		self.x_max -= 5

	def move_right(self):
		self.x_min += 5
		self.x_max += 5

	def zoom_in(self):
		self.x_min += 5
		self.x_max -= 5
		self.y_min += 5
		self.y_max -= 5

	def zoom_out(self):
		self.x_min -= 5
		self.x_max += 5
		self.y_min -= 5
		self.y_max += 5

