import pygame as pg
class Grid:
	grid_size = 8
	def __init__(self, screen_width, screen_height, dimension, isWhite, black = (0,0,0)):
		self.update_size(screen_width, screen_height)
		self.black = black
		self.isWhite = isWhite
		if isWhite:
			self.pos = {
				"a": 0,"b": 1,"c": 2,"d": 3,
				"e": 4,"f": 5,"g": 6,"h": 7,
				
				1: 7, 2: 6, 3: 5, 4: 4,
				5: 3, 6: 2, 7: 1, 8: 0
			}

			self.op_pos_x = {
				0: "a", 1: "b", 2: "c", 3: "d",
				4: "e", 5: "f", 6: "g", 7: "h"
			}

			self.op_pos_y = {
				7: 1, 6: 2, 5: 3, 4: 4,
				3: 5, 2: 6, 1: 7, 0: 8
			}
			'''
			self.op_pos = {
				"a": 7,"b": 6,"c": 5,"d": 4,
				"e": 3,"f": 2,"g": 1,"h": 0,
				
				1: 0, 2: 1, 3: 2, 4: 3,
				5: 4, 6: 5, 7: 6, 8: 7
			}
			'''
		else:
			self.pos = {
				"a": 7,"b": 6,"c": 5,"d": 4,
				"e": 3,"f": 2,"g": 1,"h": 0,
				
				1: 0, 2: 1, 3: 2, 4: 3,
				5: 4, 6: 5, 7: 6, 8: 7
			}

			self.op_pos_x = {
				7: "a", 6: "b", 5: "c", 4: "d",
				3: "e", 2: "f", 1: "g", 0: "h"
			}

			self.op_pos_y = {
				7: 8, 6: 7, 5: 6, 4: 5,
				3: 4, 2: 3, 1: 2, 0: 1
			}
			'''
			self.op_pos = {
				"a": 0,"b": 1,"c": 2,"d": 3,
				"e": 4,"f": 5,"g": 6,"h": 7,
				
				1: 7, 2: 6, 3: 5, 4: 4,
				5: 3, 6: 2, 7: 1, 8: 0
			}
			'''
		self.white = (255, 255, 255)
		self.square_side = self.side / Grid.grid_size

	def draw(self, window):
		self.square_side = self.side / Grid.grid_size
		for i in range(Grid.grid_size):
			for j in range(Grid.grid_size):
				if i % 2 == j % 2:
					pg.draw.rect(window, self.white, (self.position[0] + i * self.square_side, self.position[1] + j * self.square_side, self.square_side, self.square_side))
				else:
					pg.draw.rect(window, self.black, (self.position[0] + i * self.square_side, self.position[1] + j * self.square_side, self.square_side, self.square_side))

	def update_size(self, screen_width, screen_height):
		temp_dim = min(screen_height, screen_width)
		self.side = 0.9 * temp_dim
		self.square_side = self.side / 8
		self.set_pos(screen_width, screen_height)

	def set_pos(self, screen_width, screen_height):
		width_gap = (screen_width - self.side) / 2
		height_gap = (screen_height - self.side) / 2
		self.position = (width_gap, height_gap)

	def get_cursor_square(self, coordinates):
		x = (coordinates[0] >= self.position[0]) and (coordinates[0] <= self.position[0] + self.side)
		y = (coordinates[1] >= self.position[1]) and (coordinates[1] <= self.position[1] + self.side)
		if not (x and y):
			return -1, -1
		x = None
		y = None
		mid_x, mid_y = Grid.grid_size / 2, Grid.grid_size / 2
		len_x, len_y = Grid.grid_size / 2, Grid.grid_size / 2
		while x == None or y == None:
			if x == None:
				if mid_x != 0 and mid_x != Grid.grid_size - 1:
					if coordinates[0] < self.position[0] + mid_x * self.square_side:
						mid_x -= len_x // 2
						if len_x // 2 == 0:
							mid_x -= 1
						len_x = len_x // 2
					elif coordinates[0] > self.position[0] + mid_x * self.square_side:
						if coordinates[0] <= self.position[0] + (mid_x + 1) * self.square_side:
							x = mid_x
						else:
							mid_x += len_x // 2
							if len_x // 2 == 0:
								mid_x += 1
							len_x = len_x // 2
					else:
						return -1, -1
				elif mid_x == 0:
					if coordinates[0] < self.position[0]:
						return -1, -1
					else:
						x = 0
				else:
					if coordinates[0] > self.position[0] + self.side:
						return -1, -1
					else:
						x = Grid.grid_size - 1

			if y == None:
				if mid_y != 0 and mid_y != Grid.grid_size - 1:
					if coordinates[1] < self.position[1] + mid_y * self.square_side:
						mid_y -= len_y // 2
						if len_y // 2 == 0:
							mid_y -= 1
						len_y = len_y // 2
					elif coordinates[1] > self.position[1] + mid_y * self.square_side:
						if coordinates[1] <= self.position[1] + (mid_y + 1) * self.square_side:
							y = mid_y
						else:
							mid_y += len_y // 2
							if len_y // 2 == 0:
								mid_y += 1
							len_y = len_y // 2
					else:
						return -1, -1
				elif mid_y == 0:
					if coordinates[1] < self.position[1]:
						return -1, -1
					else:
						y = 0
				else:
					if coordinates[1] > self.position[1] + self.side:
						return -1, -1
					else:
						y = Grid.grid_size - 1
		return int(x), int(y)