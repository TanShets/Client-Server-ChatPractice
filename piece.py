from Grid import *

class Piece:
	direction = [(0,-1)]
	value = 1
	prefix = "assets/"
	postfix = ".png"
	name = ""

	def __init__(self, position, isWhite, dimension = -1):
		self.position = position
		self.isWhite = isWhite
		if isWhite:
			self.image = pg.image.load(Piece.prefix + "w_" + self.name + Piece.postfix)
		else:
			self.image = pg.image.load(Piece.prefix + "b_" + self.name + Piece.postfix)
		self.aspect = self.image.get_width() / self.image.get_height()
		self.change_scale(dimension)

	def draw(self, window, grid):
		x = grid.position[0] + self.position[0] * grid.square_side
		offset_x = grid.square_side - self.image.get_width()
		y = grid.position[1] + self.position[1] * grid.square_side
		offset_y = grid.square_side - self.image.get_height()
		window.blit(
			self.image,
			(x + int(offset_x / 2), y + int(offset_y / 2))
		)

	def change_scale(self, dimension):
		if self.aspect == 0:
			return
		else:
			self.image = pg.transform.scale(
							self.image, 
							(
								round(0.9 * dimension * self.aspect), 
								round(0.9 * dimension / self.aspect)
							)
						)

	def set_position(self, new_position):
		self.position = new_position

	def move(self):
		if self.position[1] < Grid.grid_size - 1:
			self.position = (self.position[0], self.position[1] - 1)

	def __str__(self):
		return self.name

	def capture(self):
		pass

	def get_moveset(self, piece_pos):
		if piece_pos == None:
			return []
		else:
			move_set = []
			for i in self.direction:
				vals = range(Grid.grid_size)
				a_statement = self.position[0] + i[0] in vals
				b_statement = self.position[1] + i[1] in vals
				c_statement = piece_pos.get((self.position[0] + i[0], self.position[1] + i[1]), False)
				if a_statement and b_statement and c_statement:
					piece = piece_pos[(self.position[0] + i[0], self.position[1] + i[1])]
					if piece.isWhite is not self.isWhite:
						move_set.append((self.position[0] + i[0], self.position[1] + i[1]))
				elif a_statement and b_statement:
					move_set.append((self.position[0] + i[0], self.position[1] + i[1]))
			return move_set

class Pawn(Piece):
	direction = [(0, -1), (-1, -1), (1, -1)]
	value = 1
	name = "pawn"

	def __init__(self, position, isWhite, dimension = -1):
		super().__init__(position, isWhite, dimension)
		self.hasMoved = False

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
		if self.position[1] == 0:
			return True
		else:
			return False

	def get_moveset(self, piece_pos):
		if piece_pos == None:
			return []
		else:
			move_set = []
			for i in self.direction:
				vals = range(Grid.grid_size)
				a_statement = self.position[0] + i[0] in vals
				b_statement = self.position[1] + i[1] in vals
				c_statement = piece_pos.get((self.position[0] + i[0], self.position[1] + i[1]), False)
				if a_statement and b_statement and c_statement and i != (0, -1):
					piece = piece_pos[(self.position[0] + i[0], self.position[1] + i[1])]
					if piece.isWhite is not self.isWhite:
						move_set.append((self.position[0] + i[0], self.position[1] + i[1]))
				elif a_statement and b_statement:
					move_set.append((self.position[0] + i[0], self.position[1] + i[1]))
			
			if not self.hasMoved:
				if not piece_pos.get((self.position[0], self.position[1] - 2), False):
					move_set.append((self.position[0], self.position[1] - 2))
					self.hasMoved = True
			return move_set

class Bishop(Piece):
	direction = [
		[(i, i) for i in range(1, Grid.grid_size)],
		[(-i, i) for i in range(1, Grid.grid_size)],
		[(-i, -i) for i in range(1, Grid.grid_size)],
		[(i, -i) for i in range(1, Grid.grid_size)]
	]
	value = 3
	name = "bishop"

	def get_moveset(self, piece_pos):
		if piece_pos == None:
			return []
		else:
			move_set = []
			limit = range(Grid.grid_size)
			for i in self.direction:
				for j in i:
					x = self.position[0] + j[0]
					y = self.position[1] + j[1]
					if x in limit and y in limit and piece_pos.get((x, y), False): #If there is something in the dict, its bound to be on the board
						temp_piece = piece_pos[(x, y)]
						if self.isWhite != temp_piece.isWhite:
							move_set.append((x, y))
						break
					elif x in limit and y in limit:
						move_set.append((x, y))
					else:
						break
		return move_set

class Knight(Piece):
	direction = [
		(1, 2), (2, 1), (2, -1), (1, -2),
		(-1, -2), (-2, -1), (-2, -1), (-1, -2)
	]
	value = 3
	name = "knight"

class Rook(Bishop):
	direction = [
		[(i, 0) for i in range(1, Grid.grid_size)],
		[(0, i) for i in range(1, Grid.grid_size)],
		[(-i, 0) for i in range(1, Grid.grid_size)],
		[(0, -i) for i in range(1, Grid.grid_size)]
	]
	value = 5
	name = "rook"

	def __init__(self, position, isWhite, dimension):
		super().__init__(position, isWhite, dimension)
		self.hasMoved = False

class Queen(Bishop):
	direction = [
		[(i, 0) for i in range(1, Grid.grid_size)],
		[(i, i) for i in range(1, Grid.grid_size)],
		[(0, i) for i in range(1, Grid.grid_size)],
		[(-i, i) for i in range(1, Grid.grid_size)],
		[(-i, 0) for i in range(1, Grid.grid_size)],
		[(-i, -i) for i in range(1, Grid.grid_size)],
		[(0, -i) for i in range(1, Grid.grid_size)],
		[(i, -i) for i in range(1, Grid.grid_size)]
	]
	value = 9
	name = "queen"

class King(Piece):
	direction = [
		(1, 0), (1, 1), (0, 1),
		(-1, 1), (-1, 0), (-1, -1),
		(0, -1), (1, -1)
	]
	value = 100
	name = "king"

	def __init__(self, position, isWhite, dimension):
		super().__init__(position, isWhite, dimension)
		self.hasMoved = False

def setup(isWhite, grid):
	pieces = dict()
	pieces[(grid.pos["e"], 7)] = King((grid.pos["e"], 7), isWhite, grid.square_side)
	pieces[(grid.pos["e"], 0)] = King((grid.pos["e"], 0), not isWhite, grid.square_side)

	pieces[(grid.pos["d"], 7)] = Queen((grid.pos["d"], 7), isWhite, grid.square_side)
	pieces[(grid.pos["d"], 0)] = Queen((grid.pos["d"], 0), not isWhite, grid.square_side)

	for i in ["c", "f"]:
		pieces[(grid.pos[i], 7)] = Bishop((grid.pos[i], 7), isWhite, grid.square_side)
		pieces[(grid.pos[i], 0)] = Bishop((grid.pos[i], 0), not isWhite, grid.square_side)		

	for i in ["b", "g"]:
		pieces[(grid.pos[i], 7)] = Knight((grid.pos[i], 7), isWhite, grid.square_side)
		pieces[(grid.pos[i], 0)] = Knight((grid.pos[i], 0), not isWhite, grid.square_side)

	for i in ["a", "h"]:
		pieces[(grid.pos[i], 7)] = Rook((grid.pos[i], 7), isWhite, grid.square_side)
		pieces[(grid.pos[i], 0)] = Rook((grid.pos[i], 0), not isWhite, grid.square_side)

	for i in ["a", "b", "c", "d", "e", "f", "g", "h"]:
		pieces[(grid.pos[i], 6)] = Pawn((grid.pos[i], 6), isWhite, grid.square_side)
		pieces[(grid.pos[i], 1)] = Pawn((grid.pos[i], 1), not isWhite, grid.square_side)

	return pieces