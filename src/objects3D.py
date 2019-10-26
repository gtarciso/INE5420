import objects
import viewport
import window
import clipping
import numpy as np
import math

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
		self.projected = False


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

	# fazer depois... ou não rs
	def rotateArbitraryAxis(self, theta, cx, cy, cz):

		cy_2 = cy*cy
		cz_2 = cz*cz
		d = math.sqrt(cy_2 + cz_2)

		sin_a = cy/d
		cos_a = cz/d

		sin_b = cx
		cos_b = d

		sin = np.sin(theta) 
		cos = np.cos(theta)

		r_a = np.array(([1, 0, 0, 0],
						[0, cos_a, sin_a, 0],
						[0, -sin_a, cos_a, 0],
						[0 , 0, 0, 1]), dtype = float)

		r_ainv = np.array(([1, 0, 0, 0],
						[0, cos_a, -sin_a, 0],
						[0, sin_a, cos_a, 0],
						[0 , 0, 0, 1]), dtype = float)

		r_b = np.array(([cos_b, 0, sin_b, 0],
						[0, 1, 0, 0],
						[-sin_b, 0, cos_b, 0],
						[0, 0, 0, 1]), dtype = float)

		r_binv = np.array(([cos_b, 0, -sin_b, 0],
						[0, 1, 0, 0],
						[sin_b, 0, cos_b, 0],
						[0, 0, 0, 1]), dtype = float)

		r = np.array(([cos, sin, 0, 0],
						[-sin, cos, 0, 0],
						[0, 0, 1, 0],
						[0, 0, 0, 1]), dtype = float)

		tx = float(self.x)
		ty = float(self.y)
		tz = float(self.z)
		tr_inv =  np.array((
						[ 1 ,  0 , 0, 0],
						[ 0 ,  1 , 0, 0],
						[ 0 ,  0 , 1, 0],
						[-tx, -ty, -tz, 1]), dtype = float)
		tr =  np.array((
						[ 1 ,  0 , 0, 0],
						[ 0 ,  1 , 0, 0],
						[ 0 ,  0 , 1, 0],
						[ tx, ty, tz, 1]), dtype = float)

		#point_matrix = np.array(([tx, ty, tz, 1]), dtype = float)

		#aux_matrix = np.dot(point_matrix, tr_inv)
		#aux_matrix = np.dot(aux_matrix, r_a)
		aux_matrix = np.dot(tr_inv, r_a) # ver se ta certo
		aux_matrix = np.dot(aux_matrix, r_b)
		aux_matrix = np.dot(aux_matrix, r)
		aux_matrix = np.dot(aux_matrix, r_binv)
		aux_matrix = np.dot(aux_matrix, r_ainv)
		aux_matrix = np.dot(aux_matrix, tr)

		self.x = aux_matrix[3][0]
		self.y = aux_matrix[3][1]
		self.z = aux_matrix[3][2]

		# self.x = aux_matrix[0]
		# self.y = aux_matrix[1]
		# self.z = aux_matrix[2]

		


	def rotate_scn(self, theta, cx, cy):
		tr_matrix = objects.MatrixTransform()
		rotated_matrix = tr_matrix.rotate(theta, self.x, self.y, cx, cy)
		self.scn_x = rotated_matrix[0]
		self.scn_y = rotated_matrix[1]
		

	def clip_point(self, window: window.Window):
		clip = clipping.Clipping()
		self.visible = clip.point_clipping(self.scn_x, self.scn_y, window)


	def project(self, d):
		#if self.projected == False:
		x = float(self.x)
		y = float(self.y)
		z = float(self.z)
		
		dz = z/d
		self.scn_x = (x/dz)
		self.scn_y = (y/dz)
		self.scn_z = (d)
		#	self.projected = True
		


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

	def reset_scn(self):
		for obj in self.lines:
			obj.init.reset_scn()
			obj.end.reset_scn()

	def draw_object(self, cr, viewport: viewport.Viewport):
		r = self.object_rgb[0]
		g = self.object_rgb[1]
		b = self.object_rgb[2]
		cr.save()
		cr.set_source_rgb(r, g, b)
		cr.set_line_width(0.1)
		for obj in self.lines:
			if obj.visible:
				cr.move_to(viewport.transformX(obj.init.scn_x), viewport.transformY(obj.init.scn_y))
				cr.line_to(viewport.transformX(obj.end.scn_x), viewport.transformY(obj.end.scn_y))
				#cr.move_to(viewport.transformX(obj.init.x), viewport.transformY(obj.init.y))
				#cr.line_to(viewport.transformX(obj.end.x), viewport.transformY(obj.end.y))

		cr.stroke()
		cr.restore()

	def clip_object(self, window: window.Window):
		for obj in self.lines:
			clip = clipping.Clipping()
			x_start = obj.init.scn_x
			y_start = obj.init.scn_y
			x_end = obj.end.scn_x
			y_end = obj.end.scn_y
			(visible, x1, y1, x2, y2) = clip.cohen_sutherland(x_start, y_start, x_end, y_end, window)
			obj.init.scn_x = x1
			obj.init.scn_y = y1
			obj.end.scn_x = x2
			obj.end.scn_y = y2
			obj.visible = visible

	def scale(self, sx, sy, sz):
		for obj in self.lines:
			obj.init.scale(sx, sy, sz)
			obj.end.scale(sx, sy, sz)

	def traverse(self, dx, dy, dz):
		for obj in self.lines:
			obj.init.traverse(dx, dy, dz)
			obj.end.traverse(dx, dy, dz)

	def rotateArbitraryAxis(self, theta, cx, cy, cz):
		for obj in self.lines:
			obj.init.rotateArbitraryAxis(theta, cx, cy, cz)
			obj.end.rotateArbitraryAxis(theta, cx, cy, cz)

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
		for obj in self.lines:
			obj.init.rotate_scn(theta, cx, cy)
			obj.end.rotate_scn(theta, cx, cy)

	def project(self, distance):
		for obj in self.lines:
			obj.init.project(distance)
			obj.end.project(distance)

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