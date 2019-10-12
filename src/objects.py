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
		self.visible = True

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
		self.visible = True

		self.scn_start = LinePoint(sx, sy)

		self.scn_end = LinePoint(ex, ey)


	def reset_scn(self):	
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

	def __init__(self, points, object_id, object_name, object_type, object_rgb, is_solid):
		super().__init__(object_id, object_name, object_type, object_rgb)
		self.lines = []
		self.is_solid = is_solid
		#self.scn_lines = []
		i = 1
		while i < len(points):
			new_line = Line(LinePoint(float(points[i-1].x), float(points[i-1].y)), LinePoint(float(points[i].x), float(points[i].y)), object_id, object_name, "", object_rgb)
			self.lines.append(new_line)
			i += 1

		for obj in self.lines:
			obj.reset_scn()

	def reset_scn(self):
		for obj in self.lines:
			obj.reset_scn()

	def draw_wireframe(self, cr, viewport: viewport.Viewport):
		r = self.object_rgb[0]
		g = self.object_rgb[1]
		b = self.object_rgb[2]
		cr.save()
		cr.set_source_rgb(r, g, b)
		cr.set_line_width(1)
		initial_point = None
		i = 0
		while i < len(self.lines):
			if self.lines[i].visible:
				initial_point = self.lines[i].scn_start
				break
			i += 1

		if initial_point != None:

			cr.move_to(viewport.transformX(float(initial_point.x)), viewport.transformY(float(initial_point.y)))
			while i < len(self.lines):	
				if self.lines[i].visible:
					cr.line_to(viewport.transformX(self.lines[i].scn_start.x), viewport.transformY(self.lines[i].scn_start.y))
					cr.line_to(viewport.transformX(self.lines[i].scn_end.x), viewport.transformY(self.lines[i].scn_end.y))

				i += 1	


		n = len(self.lines)-1
		if self.is_solid:
			# to check if a solid object is really solid
			if self.lines[0].start_point.x != self.lines[n].end_point.x or self.lines[0].start_point.y != self.lines[n].end_point.y:
				cr.stroke()
			else:
				cr.fill()
		else:
			cr.stroke()

		cr.restore()

	def scale(self, sx, sy):
		cx_sum = 0
		cy_sum = 0
		k = 0

		aux_list = []

		for obj in self.lines:
			aux_tuple = (obj.start_point.x, obj.start_point.y)
			#if aux_tuple not in aux_list:
			aux_list.append(aux_tuple)

			aux_tuple = (obj.end_point.x, obj.end_point.y)
			#if aux_tuple not in aux_list:
			aux_list.append(aux_tuple)


		for obj in aux_list:		
			cx_sum += obj[0]
			cy_sum += obj[1]

			k += 1

		cx = cx_sum/k
		cy = cy_sum/k

		for obj in self.lines:
			matrix_init = self.tr_matrix.scale(sx, sy, obj.start_point.x, obj.start_point.y, cx, cy)

			obj.start_point.x = matrix_init[0]
			obj.start_point.y = matrix_init[1]

			matrix_end = self.tr_matrix.scale(sx, sy, obj.end_point.x, obj.end_point.y, cx, cy)

			obj.end_point.x = matrix_end[0]
			obj.end_point.y = matrix_end[1]

	def traverse(self, dx, dy):
		for obj in self.lines:
			obj.traverse(dx, dy)

	def rotate_scn(self, theta, cx, cy):
		for obj in self.lines:
			obj.rotate_scn(theta, cx, cy)

	def clip_wireframe(self, window: window.Window):
		clip = clipping.Clipping()

		for obj in self.lines:
			obj.clip_line(window)

	def rotate(self, theta):
		cx_sum = 0
		cy_sum = 0
		k = 0

		aux_list = []

		for obj in self.lines:
			aux_tuple = (obj.start_point.x, obj.start_point.y)
			if aux_tuple not in aux_list:
				aux_list.append(aux_tuple)

			aux_tuple = (obj.end_point.x, obj.end_point.y)
			if aux_tuple not in aux_list:
				aux_list.append(aux_tuple)


		for obj in aux_list:		
			cx_sum += obj[0]
			cy_sum += obj[1]

			k += 1

		cx = cx_sum/k
		cy = cy_sum/k

		for obj in self.lines:
			obj.rotateArbitraryPoint(theta, cx, cy)


	def rotateArbitraryPoint(self, theta, cx, cy):
		for obj in self.lines:
			obj.rotateArbitraryPoint(theta, cx, cy)



class Curve(Object):

	def __init__(self, points, object_id, object_name, object_type, object_rgb, curve_type):
		super().__init__(object_id, object_name, object_type, object_rgb)
		self.points = points
		self.lines = []
		self.curve_type = curve_type
		#self.scn_lines = []
		if curve_type == "bezier":
			self.generate_bezier_curve()

		if curve_type == "b-spline":
			self.generate_bspline_curve()

	def generate_bspline_curve(self):
		mbs = np.array(([-1, 3, -3, 1],
						[ 3,-6,  3, 0],
						[-3, 0,  3, 0],
						[ 1, 4,  1, 0]), dtype = float)

		mbs = mbs/6
		
		i = 3
		dif = 0.01
		dif2 = dif*dif
		dif3 = dif2*dif

		md = np.array(( [  0 ,  0  ,   0 ,   1],
						[dif3, dif2, dif , 0  ],
						[6*dif3, 2*dif2, 0,  0],
						[6*dif3,   0,   0,   0],), dtype = float)


		#####################################################################
		#                 FORWARD DIFFERENCES IMPLEMENTATION                #
		#####################################################################

		while i < len(self.points):

			gx = np.array(( [float(self.points[i-3].x)],
							[float(self.points[i-2].x)],
							[float(self.points[i-1].x)],
							[float(self.points[i  ].x)]), dtype = float)

			gy = np.array(( [float(self.points[i-3].y)],
							[float(self.points[i-2].y)],
							[float(self.points[i-1].y)],
							[float(self.points[i  ].y)]), dtype = float) 


			cx = np.dot(mbs, gx)
			cy = np.dot(mbs, gy)


			dx = np.dot(md, cx)
			dy = np.dot(md, cy)


			j = 0

			x_ant = dx[0]
			d1x = dx[1]
			d2x = dx[2]
			d3x = dx[3]

			y_ant = dy[0]
			d1y = dy[1]
			d2y = dy[2]
			d3y = dy[3]

			x = x_ant
			y = y_ant

			while j < 1.0:
				j += dif
				x = x + d1x
				d1x = d1x + d2x
				d2x = d2x + d3x
				y = y + d1y
				d1y = d1y + d2y
				d2y = d2y + d3y
				self.lines.append(Line(LinePoint(x_ant, y_ant), LinePoint(x, y), self.object_id, self.object_name, "", self.object_rgb))
				x_ant = x
				y_ant = y


			i += 1


	def generate_bezier_curve(self):
		mb = np.array(( [-1, 3, -3, 1],
						[3, -6,  3, 0],
						[-3, 3,  0, 0],
						[1,  0,  0, 0]), dtype = float)

		gx = np.array(( [float(self.points[0].x)],
						[float(self.points[1].x)],
						[float(self.points[2].x)],
						[float(self.points[3].x)]), dtype = float)

		gy = np.array(( [float(self.points[0].y)],
						[float(self.points[1].y)],
						[float(self.points[2].y)],
						[float(self.points[3].y)]), dtype = float)

		epsilon = 0.01
		i = 0.0

		x_ant = float(self.points[0].x)
		y_ant = float(self.points[0].y)

		while i <= 1.0:
			t = self.get_t(i)
			aux = np.dot(t, mb)
			x_aux = np.dot(aux, gx)
			y_aux = np.dot(aux, gy)

			self.lines.append(Line(LinePoint(x_ant, y_ant), LinePoint(x_aux, y_aux), self.object_id, self.object_name, "", self.object_rgb))
			#self.scn_lines.append(Line(LinePoint(x_ant, y_ant), LinePoint(x_aux, y_aux), self.object_id, self.object_name, "", self.object_rgb))

			x_ant = x_aux
			y_ant = y_aux

			i += epsilon

		x_end = float(self.points[3].x)
		y_end = float(self.points[3].y)

		self.lines.append(Line(LinePoint(x_ant, y_ant), LinePoint(x_end, y_end), self.object_id, self.object_name, "", self.object_rgb))



	def get_t(self, t1):
		t2 = t1*t1
		t3 = t2*t1
		mt = np.array(([t3, t2, t1, 1]), dtype = float)
		return mt

	def reset_scn(self):
		for obj in self.lines:
			obj.reset_scn()


	def draw_curve(self, cr, viewport: viewport.Viewport):
		r = self.object_rgb[0]
		g = self.object_rgb[1]
		b = self.object_rgb[2]
		cr.save()
		cr.set_source_rgb(r, g, b)
		cr.set_line_width(1)
		initial_point = None
		i = 0
		while i < len(self.lines):
			if self.lines[i].visible:
				initial_point = self.lines[i].scn_start
				break
			i += 1

		if initial_point != None:

			cr.move_to(viewport.transformX(float(initial_point.x)), viewport.transformY(float(initial_point.y)))
			while i < len(self.lines):	
				if self.lines[i].visible:
					cr.line_to(viewport.transformX(self.lines[i].scn_start.x), viewport.transformY(self.lines[i].scn_start.y))
					cr.line_to(viewport.transformX(self.lines[i].scn_end.x), viewport.transformY(self.lines[i].scn_end.y))

				i += 1	
		
		cr.stroke()
		cr.restore()


	def rotate_scn(self, theta, cx, cy):
		for obj in self.lines:
			obj.rotate_scn(theta, cx, cy)


	def clip_curve(self, window: window.Window):
		clip = clipping.Clipping()

		for obj in self.lines:
			obj.clip_line(window)


	def traverse(self, dx, dy):
		for obj in self.lines:
			obj.traverse(dx, dy)


	def rotateArbitraryPoint(self, theta, cx, cy):
		for obj in self.lines:
			obj.rotateArbitraryPoint(theta, cx, cy)


	def rotate(self, theta):
		#initial_point = self.points[0]
		#end_point = self.points[3]
		#cx = (initial_point.x + end_point.x)/2
		#cy = (initial_point.y + end_point.y)/2

		cx_sum = 0
		cy_sum = 0
		k = 0

		aux_list = []

		for obj in self.lines:
			aux_tuple = (obj.start_point.x, obj.start_point.y)
			if aux_tuple not in aux_list:
				aux_list.append(aux_tuple)

			aux_tuple = (obj.end_point.x, obj.end_point.y)
			if aux_tuple not in aux_list:
				aux_list.append(aux_tuple)


		for obj in aux_list:		
			cx_sum += obj[0]
			cy_sum += obj[1]

			k += 1

		cx = cx_sum/k
		cy = cy_sum/k

		for obj in self.lines:
			obj.rotateArbitraryPoint(theta, cx, cy)



	def scale(self, sx, sy):
		cx_sum = 0
		cy_sum = 0
		k = 0

		aux_list = []

		for obj in self.lines:
			aux_tuple = (obj.start_point.x, obj.start_point.y)
			#if aux_tuple not in aux_list:
			aux_list.append(aux_tuple)

			aux_tuple = (obj.end_point.x, obj.end_point.y)
			#if aux_tuple not in aux_list:
			aux_list.append(aux_tuple)


		for obj in aux_list:		
			cx_sum += obj[0]
			cy_sum += obj[1]

			k += 1

		cx = cx_sum/k
		cy = cy_sum/k

		for obj in self.lines:
			matrix_init = self.tr_matrix.scale(sx, sy, obj.start_point.x, obj.start_point.y, cx, cy)

			obj.start_point.x = matrix_init[0]
			obj.start_point.y = matrix_init[1]

			matrix_end = self.tr_matrix.scale(sx, sy, obj.end_point.x, obj.end_point.y, cx, cy)

			obj.end_point.x = matrix_end[0]
			obj.end_point.y = matrix_end[1]


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



#################################################################################################################################
#                                       	            CLASSE ALTERNATIVA                                                      #
#################################################################################################################################

class Wireframe1(Object):

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
			if obj.visible and initial_point.visible:
				new_l = Line(initial_point, obj, self.object_id, self.object_name, self.object_type, self.object_rgb)
				new_l.draw_line(cr, viewport)
				initial_point = obj
				#cr.line_to(viewport.transformX(obj.x), viewport.transformY(obj.y))


		#cr.fill()
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


	def clip_wireframe(self, window: window.Window):
		clip = clipping.Clipping()
		aux = []
		i = 1

		while i < len(self.scn_points):
			start = self.scn_points[i-1]
			end = self.scn_points[i]
			x_start = float(start.x)
			y_start = float(start.y)
			x_end = float(end.x)
			y_end = float(end.y)
			(v, x1, y1, x2, y2) = clip.cohen_sutherland(x_start, y_start, x_end, y_end, window)
			st = LinePoint(x1, y1)
			st.visible = v
			ed = LinePoint(x2, y2)
			ed.visible = v
			aux.append(st)
			if i == len(self.scn_points)-1:
				aux.append(ed)
			i += 1

		self.scn_points.clear()
		for obj in aux:
			x = float(obj.x)
			y = float(obj.y)
			new_lp = LinePoint(x, y)
			new_lp.visible = obj.visible
			self.scn_points.append(new_lp)

