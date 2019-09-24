import window
import objects

class Clipping:

	#def __init__(self):
		#self.rc = [0, 0, 0, 0] # [up, down, right, left]

	def point_clipping(self, x, y, window: window.Window):
		if (window.x_min <= x and window.x_max >= x) and (window.y_min <= y and window.y_max >= y):
			return True
		else:
			return False


	def cs_left_intersec(self, x_start, y_start, x_end, y_end, x_left):
		if x_end - x_start != 0:
			m = (y_end - y_start) / (x_end - x_start)
			y = m * (x_left - x_start) + y_start
			return y
		else:
			return y_start


	def cs_right_intersec(self, x_start, y_start, x_end, y_end, x_right):
		if x_end - x_start != 0:
			m = (y_end - y_start) / (x_end - x_start)
			y = m * (x_right - x_end) + y_end
			return y
		else:
			return y_end

	def cs_up_intersec(self, x_start, y_start, x_end, y_end, y_up):
		if x_end - x_start != 0:
			m = (y_end - y_start) / (x_end - x_start)
			x = x_start + 1/m * (y_up - y_start)
			return x
		else:
			return x_start

	def cs_down_intersec(self, x_start, y_start, x_end, y_end, y_down):
		if x_end - x_start != 0:
			m = (y_end - y_start) / (x_end - x_start)
			x = x_end + 1/m * (y_down - y_end)
			return x
		else:
			return x_end

	def cohen_sutherland(self, x_start, y_start, x_end, y_end, window: window.Window):
		rc1 = [0, 0, 0, 0]
		rc2 = [0, 0, 0, 0]
		rcw = [0, 0, 0, 0] # rc window

		if x_start < window.x_min:
			rc1[3] = 1
		if x_end < window.x_min:
			rc2[3] = 1

		if x_start > window.x_max:
			rc1[2] = 1
		if x_end > window.x_max:
			rc2[2] = 1

		if y_start < window.y_min:
			rc1[1] = 1
		if y_end < window.y_min:
			rc2[1] = 1

		if y_start > window.y_max:
			rc1[0] = 1
		if y_end > window.y_max:
			rc2[0] = 1

		# verify if the line is completely inside the window
		if rc1 == rcw and rc2 == rcw:
			return (True, x_start, y_start, x_end, y_end)

		i = 0
		# verify if rc1 and rc2 != 0000

		while i < len(rcw):
			if rc1[i] and rc2[i]:
				return (False, x_start, y_start, x_end, y_end)

			i += 1


		sum_rc1 = rc1[0]+rc1[1]+rc1[2]+rc1[3]
		sum_rc2 = rc2[0]+rc2[1]+rc2[2]+rc2[3]

		if sum_rc1 > 1:
			
			(x_start, y_start) = self.get_corner(rc1, x_start, y_start, x_end, y_end, window)

		if sum_rc2 > 1:

			(x_end, y_end) = self.get_corner(rc2, x_start, y_start, x_end, y_end, window)
		# index 0 = top, 1 = down, 2 = right, 3 = left
		# start point
		if sum_rc1 == 1:
			if rc1[0] == 1:
				x_start = self.cs_up_intersec(x_start, y_start, x_end, y_end, window.y_max)
				y_start = window.y_max

			if rc1[1] == 1:
				x_start = self.cs_down_intersec(x_start, y_start, x_end, y_end, window.y_min)
				y_start = window.y_min

			if rc1[2] == 1:
				y_start = self.cs_right_intersec(x_start, y_start, x_end, y_end, window.x_max)
				x_start = window.x_max

			if rc1[3] == 1:
				y_start = self.cs_left_intersec(x_start, y_start, x_end, y_end, window.x_min)
				x_start = window.x_min

		# end point
		if sum_rc2 == 1:
			if rc2[0] == 1:
				x_end = self.cs_up_intersec(x_start, y_start, x_end, y_end, window.y_max)
				y_end = window.y_max

			if rc2[1] == 1:
				x_end = self.cs_down_intersec(x_start, y_start, x_end, y_end, window.y_min)
				y_end = window.y_min

			if rc2[2] == 1:
				y_end = self.cs_right_intersec(x_start, y_start, x_end, y_end, window.x_max)
				x_end = window.x_max

			if rc2[3] == 1:
				y_end = self.cs_left_intersec(x_start, y_start, x_end, y_end, window.x_min)
				x_end = window.x_min


		return (True, x_start, y_start, x_end, y_end)


	def get_corner(self, rc, x_start, y_start, x_end, y_end, window: window.Window):
		
		# index 0 = top, 1 = down, 2 = right, 3 = left
		# rc = top and right
		x = window.x_min
		y = window.y_min
		if rc[0] == 1 and rc[2] == 1:
			x = self.cs_up_intersec(x_start, y_start, x_end, y_end, window.y_max)
			y = self.cs_right_intersec(x_start, y_start, x_end, y_end, window.x_max)
			if x > window.x_max:
				x = window.x_max
			if y > window.y_max:
				y = window.y_max
			return (x, y)

		if rc[0] == 1 and rc[3] == 1:
			x = self.cs_up_intersec(x_start, y_start, x_end, y_end, window.y_max)
			y = self.cs_left_intersec(x_start, y_start, x_end, y_end, window.x_min)
			if x < window.x_min:
				x = window.x_min
			if y > window.y_max:
				y = window.y_max
			return (x, y)

		if rc[1] == 1 and rc[2] == 1:
			x = self.cs_down_intersec(x_start, y_start, x_end, y_end, window.y_min)
			y = self.cs_right_intersec(x_start, y_start, x_end, y_end, window.x_max)
			if x > window.x_max:
				x = window.x_max
			if y < window.y_min:
				y = window.y_min
			return (x, y)

		if rc[1] == 1 and rc[3] == 1:
			x = self.cs_down_intersec(x_start, y_start, x_end, y_end, window.y_min)
			y = self.cs_left_intersec(x_start, y_start, x_end, y_end, window.x_min)
			if x < window.x_min:
				x = window.x_min
			if y < window.y_min:
				y = window.y_min
			return (x, y)
