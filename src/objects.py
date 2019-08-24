import viewport	
import numpy as np

class Object:

	def __init__(self, object_id, object_name, object_type):
		self.object_id = object_id
		self.object_name = object_name
		self.object_type = object_type
		self.tr_matrix = MatrixTransform()

class LinePoint:

	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

class Point(Object):

	def __init__ (self, x: float, y: float, object_id, object_name, object_type):
		super().__init__(object_id, object_name, object_type)
		self.x = x
		self.y = y

	def draw_point(self, cr, viewport: viewport.Viewport):
		cr.save()
		cr.set_source_rgb(1, 1, 1)
		cr.set_line_width(1)
		cr.move_to(viewport.transformX(self.x), viewport.transformY(self.y))
		cr.line_to(viewport.transformX(self.x+0.25), viewport.transformY(self.y))
		cr.stroke()
		cr.restore()

	def scale(self, sx, sy):
		scaled_matrix = self.tr_matrix.scale(sx, sy, self.x, self.y)
		self.x = scaled_matrix[0]
		self.y = scaled_matrix[1]

	def traverse(self, dx, dy):
		traversed_matrix = self.tr_matrix.traverse(dx, dy, self.x, self.y)
		self.x = traversed_matrix[0]
		self.y = traversed_matrix[1]

	def rotate(self, theta):
		rotated_matrix = self.tr_matrix.traverse(self.x, self.y, theta)
		self.x = rotated_matrix[0]
		self.y = rotated_matrix[1]

class Line(Object):

	def __init__(self, start_point: LinePoint, end_point: LinePoint, object_id, object_name, object_type):
		super().__init__(object_id, object_name, object_type)
		self.start_point = start_point
		self.end_point = end_point

	def draw_line(self, cr, viewport: viewport.Viewport):
		cr.save()
		cr.set_source_rgb(1, 1, 1)
		cr.set_line_width(1)
		cr.move_to(viewport.transformX(self.start_point.x), viewport.transformY(self.start_point.y))
		cr.line_to(viewport.transformX(self.end_point.x), viewport.transformY(self.end_point.y))
		cr.stroke()
		cr.restore()

	def scale(self, sx, sy):
		matrix_init = self.tr_matrix.scale(sx, sy, self.start_point.x, self.start_point.y)
		self.start_point.x = matrix_init[0]
		self.start_point.y = matrix_init[1]

		matrix_end = self.tr_matrix.scale(sx, sy, self.end_point.x, self.end_point.y)
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
		print("TODO")

class Wireframe(Object):

	def __init__(self, points, object_id, object_name, object_type):
		super().__init__(object_id, object_name, object_type)
		self.points = points

	def draw_wireframe(self, cr, viewport: viewport.Viewport):
		cr.save()
		cr.set_source_rgb(1, 1, 1)
		cr.set_line_width(1)
		initial_point = self.points[0]
		cr.move_to(viewport.transformX(initial_point.x), viewport.transformY(initial_point.y))

		for obj in self.points:
			cr.line_to(viewport.transformX(obj.x), viewport.transformY(obj.y))

		cr.stroke()
		cr.restore()


class MatrixTransform:

	def scale(self, sx, sy, x, y):
		param_matrix = np.array((
			[sx, 0, 0],
			[0, sy, 0],
			[0, 0 , 1]), dtype = float)

		point_matrix = np.array(([x, y, 1]), dtype = float)
		scaled_matrix = np.dot(point_matrix, param_matrix)

		return scaled_matrix

	def traverse(self, dx, dy, x, y):
		param_matrix = np.array((
			[1,  0 , 0],
			[0,  1 , 1],
			[dx, dy, 1]), dtype = float)

		point_matrix = np.array(([x, y, 1]), dtype = float)
		traversed_matrix = np.dot(point_matrix, param_matrix)

		return traversed_matrix

	def rotation(self, x, y, theta):
		sin = np.sin(theta) 
		cos = np.cos(theta)
		param_matrix = np.array((
			[cos, -sin, 0],
			[sin,  cos, 0],
			[ 0 ,   0 , 1]), dtype = float)

		point_matrix = np.array(([x, y, 1]), dtype = float)
		rotated_matrix = np.dot(point_matrix, param_matrix)

		return rotated_matrix
