import objects

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

	def scale(self, sx, sy):
		print("TODO")

	def traverse(self, dx, dy):
		print("TODO")

	def rotate(self, theta):
		print("TODO")

	def rotateArbitraryPoint(self, theta, x, y):
		print("TODO")

	def rotate_scn(self, theta, cx, cy):
		print("TODO")

	def clip_point(self, window: window.Window):
		print("TODO")