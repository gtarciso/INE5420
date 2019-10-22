import objects

class Window:

	def __init__(self, xmin, ymin, xmax, ymax):
		self.x_min = xmin
		self.x_max = xmax
		self.y_min = ymin
		self.y_max = ymax
		self.wHeight = ymax-ymin
		self.wWidth = xmax - xmin

		self.zoom_value = 1.1
		self.theta = 0.0
		self.window_center = objects.LinePoint((self.x_max - self.x_min)/2, (self.y_max - self.y_min)/2)
		#self.vup = objects.Line(objects.LinePoint(self.x_min, self.y_min), objects.LinePoint(self.x_min, self.y_max), -1, "", "", [1, 1, 1])


		self.tr_matrix = objects.MatrixTransform()

	def reset(self, xmin, ymin, xmax, ymax):
		self.x_min = xmin
		self.x_max = xmax
		self.y_min = ymin
		self.y_max = ymax
		self.zoom_value = 1.1
		self.theta = 0.0
		self.window_center = objects.LinePoint((self.x_max - self.x_min)/2, (self.y_max - self.y_min)/2)
		#self.vup = objects.Line(objects.LinePoint(self.x_min, self.y_min), objects.LinePoint(self.x_min, self.y_max), -1, "", "", [1, 1, 1])

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
		self.x_min /= self.zoom_value
		self.x_max /= self.zoom_value
		self.y_min /= self.zoom_value
		self.y_max /= self.zoom_value

	def zoom_out(self):
		self.x_min *= self.zoom_value
		self.x_max *= self.zoom_value
		self.y_min *= self.zoom_value
		self.y_max *= self.zoom_value

	def rotate(self, theta):
		self.theta += theta

	def set_atributes(self, x1, x2, y1, y2):
		self.x_min = x1
		self.x_max = x2
		self.y_min = y1
		self.y_max = y2
		self.window_center = objects.LinePoint((self.x_max - self.x_min)/2, (self.y_max - self.y_min)/2)



