import viewport	

class Object:

	def __init__(self, object_id, object_name, object_type):
		self.object_id = object_id
		self.object_name = object_name
		self.object_type = object_type

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
		print(viewport.transformX(self.y))
		cr.move_to(viewport.transformX(self.x), viewport.transformY(self.y))
		cr.line_to(viewport.transformX(self.x+0.25), viewport.transformY(self.y))
		cr.stroke()
		cr.restore()

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
