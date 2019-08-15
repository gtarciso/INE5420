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

	def draw_point(self, cr):
		cr.save()
		cr.set_source_rgb(1, 1, 1)
		cr.set_line_width(1)
		cr.move_to(self.x, self.y)
		cr.line_to(self.x+1, self.y)
		cr.stroke()
		cr.restore()

class Line(Object):

	def __init__(self, start_point: LinePoint, end_point: LinePoint, object_id, object_name, object_type):
		super().__init__(object_id, object_name, object_type)
		self.start_point = start_point
		self.end_point = end_point

	def draw_line(self, cr):
		cr.save()
		cr.set_source_rgb(1, 1, 1)
		cr.set_line_width(1)
		cr.move_to(self.start_point.x, self.start_point.y)
		cr.line_to(self.end_point.x, self.end_point.y)
		cr.stroke()
		cr.restore()

class Polygon(Object):

	def __init__(self, points, object_id, object_name, object_type):
		super().__init__(object_id, object_name, object_type)
		self.points = points
