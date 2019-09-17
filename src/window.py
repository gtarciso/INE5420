import objects

class Window:

	def __init__(self, xmin, ymin, xmax, ymax):
		self.x_min = xmin
		self.x_max = xmax
		self.y_min = ymin
		self.y_max = ymax
		self.zoom_value = 1.1
		self.theta = 0.0
		self.tr_matrix = objects.MatrixTransform()

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
		self.theta = theta
		cx = (self.x_max - self.x_min)/2
		cy = (self.y_max - self.y_min)/2

		max_coordinates = self.tr_matrix.rotate(theta, self.x_max, self.y_max, cx, cy)
		min_coordinates = self.tr_matrix.rotate(theta, self.x_min, self.y_min, cx, cy)

		self.x_max = max_coordinates[0]
		self.x_min = min_coordinates[0]

		self.y_max = max_coordinates[1]
		self.y_min = min_coordinates[1]
		print(self.x_min)
		print(self.x_max)
		print(self.x_max + self.x_min)
		print("")
		print(self.y_min)
		print(self.y_max)
		print(self.y_max + self.y_min)
