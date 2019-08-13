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

class Line(Object):

	def __init__(self, start_point: LinePoint, end_point: LinePoint, object_id, object_name, object_type):
		super().__init__(object_id, object_name, object_type)
		self.start_point = start_point
		self.end_point = end_point

class Polygon(Object):

	def __init__(self, points, object_id, object_name, object_type):
		super().__init__(object_id, object_name, object_type)
		self.points = points
