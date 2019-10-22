import objects
import viewport
import window
import numpy as np

class Point3D(objects.Object):

	def __init__(self, x: float, y: float, z: float, object_id, object_name, object_type, object_rgb):
		super().__init__(object_id, object_name, object_type, object_rgb)
		self.x = x
		self.y = y
		self.z = z
		self.scn_x = x
		self.scn_y = y
		self.scn_z = z
		self.visible = True


	def reset_scn(self):
		self.scn_x = self.x
		self.scn_y = self.y
		self.scn_z = self.z

	def draw_point(self, cr, viewport: viewport.Viewport):
		print("TODO")

	def scale(self, sx, sy, sz):
		(self.x, self.y, self.z) = MatrixTransform3D.scale(sx, sy, sz, self.x, self.y, self.z)

	def traverse(self, dx, dy, dz):
		(self.x, self.y, self.z) = MatrixTransform3D.traverse(dx, dy, dz, self.x, self.y, self.z)

	def rotate_x(self, theta):
		rotated_matrix = MatrixTransform3D.rotate_x(theta, self.x, self.y, self.z)
		self.x = rotated_matrix[0]
		self.y = rotated_matrix[1]
		self.z = rotated_matrix[2]

	def rotate_y(self, theta):
		rotated_matrix = MatrixTransform3D.rotate_y(theta, self.x, self.y, self.z)
		self.x = rotated_matrix[0]
		self.y = rotated_matrix[1]
		self.z = rotated_matrix[2]

	def rotate_z(self, theta):
		rotated_matrix = MatrixTransform3D.rotate_z(theta, self.x, self.y, self.z)
		self.x = rotated_matrix[0]
		self.y = rotated_matrix[1]
		self.z = rotated_matrix[2]

	def rotateArbitraryPoint(self, theta, x, y):
		print("TODO")

	def rotate_scn(self, theta, cx, cy):
		print("TODO")

	def clip_point(self, window: window.Window):
		print("TODO")


# lines as list of tuples of 3dpoints?

class Line3D():
	def __init__(self, init: Point3D, end: Point3D):
		self.init = init
		self.end = end
		self.visible = True

class Object3D(objects.Object):
	def __init__(self, lines, object_id, object_name, object_type, object_rgb):
		super().__init__(object_id, object_name, object_type, object_rgb)
		self.lines = lines

	def draw_object(self, cr, viewport: viewport.Viewport):
		r = self.object_rgb[0]
		g = self.object_rgb[1]
		b = self.object_rgb[2]
		cr.save()
		cr.set_source_rgb(r, g, b)
		cr.set_line_width(0.1)
		for obj in self.lines:
			#cr.move_to(viewport.transformX(obj.init.scn_x), viewport.transformY(obj.init.scn_y))
			#cr.line_to(viewport.transformX(obj.end.scn_x), viewport.transformY(obj.end.scn_y))
			cr.move_to(viewport.transformX(obj.init.x), viewport.transformY(obj.init.y))
			cr.line_to(viewport.transformX(obj.end.x), viewport.transformY(obj.end.y))

		cr.stroke()
		cr.restore()

	def scale(self, sx, sy, sz):
		for obj in self.lines:
			obj.init.scale(sx, sy, sz)
			obj.end.scale(sx, sy, sz)

	def traverse(self, dx, dy, dz):
		for obj in self.lines:
			obj.init.traverse(dx, dy, dz)
			obj.end.traverse(dx, dy, dz)

	def rotate_x(self, theta):
		for obj in self.lines:
			obj.init.rotate_x(theta)
			obj.end.rotate_x(theta)

	def rotate_y(self, theta):
		for obj in self.lines:
			obj.init.rotate_y(theta)
			obj.end.rotate_y(theta)


	def rotate_z(self, theta):
		for obj in self.lines:
			obj.init.rotate_z(theta)
			obj.end.rotate_z(theta)

	def rotate_scn(self, theta, cx, cy):
		print("do nothing")


class MatrixTransform3D:

	def scale(sx, sy, sz, x, y, z):
		x1 = sx * x
		y1 = sy * y
		z1 = sz * z
		return (x1, y1, z1)

	def traverse(tx, ty, tz, x, y, z):
		x1 = tx + x
		y1 = ty + y
		z1 = tz + z
		return (x1, y1, z1)

	def rotate_x(theta, x, y, z):
		sin = np.sin(theta) 
		cos = np.cos(theta)
		point_matrix = np.array(([x, y, z, 1]), dtype = float)
		param_matrix = np.array(([1, 0, 0, 0],
								[0, cos, sin, 0],
								[0, -sin, cos, 0],
								[0, 0, 0, 1]), dtype = float)

		rotated_matrix = np.dot(point_matrix, param_matrix)
		return rotated_matrix


	def rotate_y(theta, x, y, z):
		sin = np.sin(theta) 
		cos = np.cos(theta)
		point_matrix = np.array(([x, y, z, 1]), dtype = float)
		param_matrix = np.array(([cos, 0, -sin, 0],
								[0, 1, 0, 0],
								[sin, 0, cos, 0],
								[0, 0, 0, 1]), dtype = float)

		rotated_matrix = np.dot(point_matrix, param_matrix)
		return rotated_matrix


	def rotate_z(theta, x, y, z):
		sin = np.sin(theta) 
		cos = np.cos(theta)
		point_matrix = np.array(([x, y, z, 1]), dtype = float)
		param_matrix = np.array(([cos, sin, 0, 0],
								[-sin, cos, 0, 0],
								[0, 0, 1, 0],
								[0, 0, 0, 1]), dtype = float)

		rotated_matrix = np.dot(point_matrix, param_matrix)
		return rotated_matrix