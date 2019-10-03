import objects
import window

class objectDescriptor():

	def load_file(self, file_name):
		vertex = []
		window = None
		objects = []
		object_id = 0

		with open(file_name, "r") as f:
			text = f.read()

			for line in text.splitlines():
				ln = line.split(" ")
				command = ln[0]

				if command == "v":
					print("TODO, FALTA OS PONTO 3D")


	def save_file(self, file_name, window: window.Window, objects):
		with open(file_name, "w+") as f: