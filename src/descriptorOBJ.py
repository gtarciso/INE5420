import objects3D
import window

class objectDescriptor():

	def load_file(file_name, obj_id):
		lines = []
		vertex = []
		window = None
		objects = []
		object_id = obj_id
		object_name = ''
		flag_obj_changed = 0
		object_rgb = [0, 0, 1]
		index = 0
		with open(file_name, "r") as f:
			text = f.read()

			for line in text.splitlines():
				ln = line.split(" ")
				command = ln[0]

				if command == "v":
					vertex.append((ln[1], ln[2], ln[3]))

				if command == "o":
					if len(lines) > 0:
						aux_list = []
						for obj in lines:
							aux_list.append(obj)
						new_obj = objects3D.Object3D(aux_list, object_id, object_name, "3D Object", object_rgb)
						objects.append(new_obj) 

						lines.clear()
					object_name = ln[1]

				if command == "f":

					for i in range(1, len(ln)):
						p = ln[i].split('/')
						p1 = int(p[0])-1
						p2 = int(p[1])-1
						p3 = int(p[2])-1

						x1 = float(vertex[p1][0])
						y1 = float(vertex[p1][1])
						z1 = float(vertex[p1][2])

						x2 = float(vertex[p2][0])
						y2 = float(vertex[p2][1])
						z2 = float(vertex[p2][2])
						
						x3 = float(vertex[p3][0])
						y3 = float(vertex[p3][1])
						z3 = float(vertex[p3][2])

						point1 = objects3D.Point3D(x1, y1, z1, object_id, object_name, "3D Object", object_rgb)
						point2 = objects3D.Point3D(x2, y2, z2, object_id, object_name, "3D Object", object_rgb)
						point3 = objects3D.Point3D(x3, y3, z3, object_id, object_name, "3D Object", object_rgb)

						lines.append(objects3D.Line3D(point1, point2))
						lines.append(objects3D.Line3D(point1, point3))
						lines.append(objects3D.Line3D(point2, point3))



				if command == "w":
					center_x = float(vertex[int(ln[1])-1][0])
					center_y = float(vertex[int(ln[1])-1][1])

					size_x = float(vertex[int(ln[2])-1][0])/2
					size_y = float(vertex[int(ln[2])-1][1])/2

					x_min = center_x - size_x
					x_max = center_x + size_x
					y_min = center_y - size_y
					y_max = center_y + size_y
					window = (x_min, x_max, y_min, y_max)

		return (objects, window)



	def save_file(self, file_name, window: window.Window, objects):
		with open(file_name, "w+") as f:
			print("NONE")