import Grid

class Piece:
	def __init__(self, name, position, isWhite, value = 1):
		self.name = name
		self.position = position
		self.value = value
		self.isWhite = isWhite

	def set_position(self, new_position):
		self.position = new_position

	def move(self):
		if self.position[1] < Grid.Grid.grid_size - 1:
			self.position = (self.position[0], self.position[1] + 1)

	def capture(self):
		pass

class Pawn(Piece):
	def __init__(self, position, isWhite):
		self.name = "Pawn"
		self.isWhite = isWhite
		self.position = position
		self.value = 1

	def capture(self, capture_id = 0):
		pass

	def move(self, isCapture = False, capture_id = 0):
		if not isCapture:
			super().move()
			if self.isPromoted():
				return True
			else:
				return False
		else:
			self.capture(capture_id)
			return False

	def isPromoted(self):
		if self.position[1] == Grid.Grid.grid_size - 1:
			return True
		else:
			return False

piece = Pawn((3, 5), True)
print(piece.position)
piece.set_position((1,6))
print(piece.position)
piece.move()
print(piece.position)
piece.move()
print(piece.position)