import window

class Viewport:

	def __init__(self, xmin, xmax, ymin, ymax, window: window.Window):

		self.x_min = xmin
		self.y_min = ymin
		self.x_max = xmax
		self.y_max = ymax

		self.window = window


	def transformX(self, x):
		xw_min = self.window.x_min
		xw_max = self.window.x_max

		try:
			x_vp = ((x - xw_min) / (xw_max - xw_min)) * (self.x_max - self.x_min)
			return x_vp

		except ZeroDivisionError:
			pass


	def transformY(self, y):
		yw_min = self.window.y_min
		yw_max = self.window.y_max

		try:
			y_vp = (1 - (y - yw_min) / (yw_max - yw_min)) * (self.y_max - self.y_min) 
			return y_vp

		except ZeroDivisionError:
			pass