import viewport
import window	
import clipping
import numpy as np

class Object:

	def __init__(self, object_id, object_name, object_type, object_rgb):
		self.object_id = object_id
		self.object_name = object_name
		self.object_type = object_type
		self.object_rgb = object_rgb
		self.tr_matrix = MatrixTransform()

class LinePoint:

	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

class Point(Object):

	def __init__ (self, x: float, y: float, object_id, object_name, object_type, object_rgb):
		super().__init__(object_id, object_name, object_type, object_rgb)
		self.x = x
		self.y = y
		self.scn_x = x
		self.scn_y = y
		self.visible = True

	def reset_scn(self):
		self.scn_x = self.x
		self.scn_y = self.y

	def draw_point(self, cr, viewport: viewport.Viewport):
		r = self.object_rgb[0]
		g = self.object_rgb[1]
		b = self.object_rgb[2]
		cr.save()
		cr.set_source_rgb(r, g, b)
		cr.set_line_width(1)
		cr.move_to(viewport.transformX(self.scn_x), viewport.transformY(self.scn_y))
		cr.line_to(viewport.transformX(self.scn_x+0.25), viewport.transformY(self.scn_y))
		cr.stroke()
		cr.restore()

	def scale(self, sx, sy):
		#@param scale(sx, sy, x, y, cx, cy) | cx, cy = center of the object
		scaled_matrix = self.tr_matrix.scale(sx, sy, self.x, self.y, self.x, self.y)
		self.x = scaled_matrix[0]
		self.y = scaled_matrix[1]

	def traverse(self, dx, dy):
		traversed_matrix = self.tr_matrix.traverse(dx, dy, self.x, self.y)
		self.x = traversed_matrix[0]
		self.y = traversed_matrix[1]

	def rotate(self, theta):
		self.rotateArbitraryPoint(theta, self.x, self.y)

	def rotateArbitraryPoint(self, theta, x, y):
		rotated_matrix = self.tr_matrix.rotate(theta, self.x, self.y, x, y)
		self.x = rotated_matrix[0]
		self.y = rotated_matrix[1]

	def rotate_scn(self, theta, cx, cy):
		rotated_matrix = self.tr_matrix.rotate(theta, self.x, self.y, cx, cy)
		self.scn_x = rotated_matrix[0]
		self.scn_y = rotated_matrix[1]

	def clip_point(self, window: window.Window):
		clip = clipping.Clipping()
		self.visible = clip.point_clipping(self.scn_x, self.scn_y, window)

class Line(Object):

	def __init__(self, start_point: LinePoint, end_point: LinePoint, object_id, object_name, object_type, object_rgb):
		super().__init__(object_id, object_name, object_type, object_rgb)
		self.start_point = start_point
		self.end_point = end_point
		sx = float(start_point.x)
		sy = float(start_point.y)
		ex = float(end_point.x)
		ey = float(end_point.y)

		self.scn_start = LinePoint(sx, sy)

		self.scn_end = LinePoint(ex, ey)


	def reset_scn(self):
		if self.scn_start.x == self.start_point.x:
			print("error")
			print(self.start_point.x)
		self.scn_start.x = float(self.start_point.x)
		self.scn_start.y = float(self.start_point.y)
		self.scn_end.x = float(self.end_point.x)
		self.scn_end.y = float(self.end_point.y)


	def draw_line(self, cr, viewport: viewport.Viewport):
		r = self.object_rgb[0]
		g = self.object_rgb[1]
		b = self.object_rgb[2]
		cr.save()
		cr.set_source_rgb(r, g, b)
		cr.set_line_width(1)
		cr.move_to(viewport.transformX(self.scn_start.x), viewport.transformY(self.scn_start.y))
		cr.line_to(viewport.transformX(self.scn_end.x), viewport.transformY(self.scn_end.y))
		cr.stroke()
		cr.restore()

	def scale(self, sx, sy):
		cx = (self.start_point.x + self.end_point.x)/2
		cy = (self.start_point.y + self.end_point.y)/2

		matrix_init = self.tr_matrix.scale(sx, sy, self.start_point.x, self.start_point.y, cx, cy)

		self.start_point.x = matrix_init[0]
		self.start_point.y = matrix_init[1]

		matrix_end = self.tr_matrix.scale(sx, sy, self.end_point.x, self.end_point.y, cx, cy)

		self.end_point.x = matrix_end[0]
		self.end_point.y = matrix_end[1]

	def traverse(self, dx, dy):
		matrix_init = self.tr_matrix.traverse(dx, dy, self.start_point.x, self.start_point.y)
		self.start_point.x = matrix_init[0]
		self.start_point.y = matrix_init[1]

		matrix_end = self.tr_matrix.traverse(dx, dy, self.end_point.x, self.end_point.y)
		self.end_point.x = matrix_end[0]
		self.end_point.y = matrix_end[1]


	def rotate(self, theta):
		cx = (self.start_point.x + self.end_point.x)/2
		cy = (self.start_point.y + self.end_point.y)/2

		self.rotateArbitraryPoint(theta, cx, cy)


	def rotateArbitraryPoint(self, theta, cx, cy):
		matrix_init = self.tr_matrix.rotate(theta, self.start_point.x, self.start_point.y, cx, cy)
		self.start_point.x = matrix_init[0]
		self.start_point.y = matrix_init[1]

		matrix_end = self.tr_matrix.rotate(theta, self.end_point.x, self.end_point.y, cx, cy)
		self.end_point.x = matrix_end[0]
		self.end_point.y = matrix_end[1]

	def rotate_scn(self, theta, cx, cy):
		matrix_init = self.tr_matrix.rotate(theta, self.start_point.x, self.start_point.y, cx, cy)
		self.scn_start.x = matrix_init[0]
		self.scn_start.y = matrix_init[1]

		matrix_end = self.tr_matrix.rotate(theta, self.end_point.x, self.end_point.y, cx, cy)
		self.scn_end.x = matrix_end[0]
		self.scn_end.y = matrix_end[1]


	def clip_line(self, window: window.Window):
		clip = clipping.Clipping()
		x_start = self.scn_start.x
		y_start = self.scn_start.y
		x_end = self.scn_end.x
		y_end = self.scn_end.y
		(self.visible, x1, y1, x2, y2) = clip.cohen_sutherland(x_start, y_start, x_end, y_end, window)
		self.scn_start.x = x1
		self.scn_start.y = y1
		self.scn_end.x = x2
		self.scn_end.y = y2


class Wireframe(Object):

	def __init__(self, points, object_id, object_name, object_type, object_rgb):
		super().__init__(object_id, object_name, object_type, object_rgb)
		self.points = points

		self.scn_points = []
		for obj in points:
			x = float(obj.x)
			y = float(obj.y)
			self.scn_points.append(LinePoint(x, y))

	def reset_scn(self):
		self.scn_points.clear()
		for obj in self.points:
			x = float(obj.x)
			y = float(obj.y)
			self.scn_points.append(LinePoint(x, y))

	def draw_wireframe(self, cr, viewport: viewport.Viewport):
		r = self.object_rgb[0]
		g = self.object_rgb[1]
		b = self.object_rgb[2]
		cr.save()
		cr.set_source_rgb(r, g, b)
		cr.set_line_width(1)
		initial_point = self.scn_points[0]
		cr.move_to(viewport.transformX(initial_point.x), viewport.transformY(initial_point.y))

		for obj in self.scn_points:
			cr.line_to(viewport.transformX(obj.x), viewport.transformY(obj.y))

		cr.stroke()
		cr.restore()

	def scale(self, sx, sy):
		cx_sum = 0
		cy_sum = 0
		k = 0
		for obj in self.points:
			cx_sum += obj.x
			cy_sum += obj.y
			k += 1

		cx = cx_sum/k
		cy = cy_sum/k

		for obj in self.points:
			scaled_matrix = self.tr_matrix.scale(sx, sy, obj.x, obj.y, cx, cy)
			obj.x = scaled_matrix[0]
			obj.y = scaled_matrix[1]


	def traverse(self, dx, dy):
		for obj in self.points:
			traversed_matrix = self.tr_matrix.traverse(dx, dy, obj.x, obj.y)
			obj.x = traversed_matrix[0]
			obj.y = traversed_matrix[1]


	def rotate(self, theta):
		cx_sum = 0
		cy_sum = 0
		k = 0

		aux_list = []

		for obj in self.points:
			aux_tuple = (obj.x, obj.y)
			if aux_tuple not in aux_list:
				aux_list.append(aux_tuple)

		for obj in aux_list:		
			cx_sum += obj[0]
			cy_sum += obj[1]

			k += 1

		cx = cx_sum/k
		cy = cy_sum/k

		self.rotateArbitraryPoint(theta, cx, cy)

			

	def rotateArbitraryPoint(self, theta, cx, cy):

		for obj in self.points:
			rotated_matrix = self.tr_matrix.rotate(theta, obj.x, obj.y, cx, cy)
			obj.x = rotated_matrix[0]
			obj.y = rotated_matrix[1]

	def rotate_scn(self, theta, cx, cy):
		i = 0
		while i < len(self.scn_points):
			rotated_matrix = self.tr_matrix.rotate(theta, self.points[i].x, self.points[i].y, cx, cy)
			self.scn_points[i].x = rotated_matrix[0]
			self.scn_points[i].y = rotated_matrix[1]
			i += 1



class MatrixTransform:

	def scale(self, sx, sy, x, y, cx, cy):
		tr_mt1 = np.array((
			[ 1 ,  0 , 0],
			[ 0 ,  1 , 0],
			[-cx, -cy, 1]), dtype = float)

		tr_mt2 = np.array((
			[1 , 0 , 0],
			[0 , 1 , 0],
			[cx, cy, 1]), dtype = float)

		param_matrix = np.array((
			[sx, 0, 0],
			[0, sy, 0],
			[0, 0 , 1]), dtype = float)

		point_matrix = np.array(([x, y, 1]), dtype = float)
		aux_matrix = np.dot(point_matrix, tr_mt1)
		aux_matrix = np.dot(aux_matrix, param_matrix)
		scaled_matrix = np.dot(aux_matrix, tr_mt2)

		return scaled_matrix

	def traverse(self, dx, dy, x, y):
		param_matrix = np.array((
			[1,  0 , 0],
			[0,  1 , 1],
			[dx, dy, 1]), dtype = float)

		point_matrix = np.array(([x, y, 1]), dtype = float)
		traversed_matrix = np.dot(point_matrix, param_matrix)

		return traversed_matrix

	def rotate(self, theta, x, y, cx, cy):
		sin = np.sin(theta) 
		cos = np.cos(theta)

		tr_mt1 = np.array((
			[ 1 ,  0 , 0],
			[ 0 ,  1 , 0],
			[-cx, -cy, 1]), dtype = float)

		tr_mt2 = np.array((
			[1 , 0 , 0],
			[0 , 1 , 0],
			[cx, cy, 1]), dtype = float)

		param_matrix = np.array((
			[cos, -sin, 0],
			[sin,  cos, 0],
			[ 0 ,   0 , 1]), dtype = float)

		point_matrix = np.array(([x, y, 1]), dtype = float)

		aux_matrix = np.dot(point_matrix, tr_mt1)
		aux_matrix = np.dot(aux_matrix, param_matrix)
		rotated_matrix = np.dot(aux_matrix, tr_mt2)

		return rotated_matrix
