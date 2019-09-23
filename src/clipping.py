import window

class Clipping:

	def __init__(self):
		self.rc = [0, 0, 0, 0] # [up, down, right, left]

	def point_clipping(self, x, y, window: window.Window):
		if (window.x_min <= x and window.x_max >= x) and (window.y_min <= y and window.y_max >= y):
			return True
		else:
			return False

