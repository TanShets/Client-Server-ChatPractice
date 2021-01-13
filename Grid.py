import pygame as pg
class Grid:
	grid_size = 8
	pos = {
		"a": 0,"b": 1,"c": 2,"d": 3,
		"e": 4,"f": 5,"g": 6,"h": 7,
		
		1: 0, 2: 1, 3: 2, 4: 3,
		5: 4, 6: 5, 7: 6, 8: 7
	}
	def __init__(self, screen_width, screen_height, dimension, isWhite, black = (0,0,0)):
		self.update_size(screen_width, screen_height)
		self.black = black
		self.isWhite = isWhite
		self.white = (255, 255, 255)

	def draw(self, window):
		square_width = self.width / Grid.grid_size
		square_height = self.height / Grid.grid_size
		print(square_width, square_height)
		for i in range(Grid.grid_size):
			for j in range(Grid.grid_size):
				if (self.isWhite and i % 2 == j % 2) or (not self.isWhite and i % 2 != j % 2):
					pg.draw.rect(window, self.white, (self.position[0] + i * square_width, self.position[1] + j * square_height, square_width, square_height))
				else:
					pg.draw.rect(window, self.black, (self.position[0] + i * square_width, self.position[1] + j * square_height, square_width, square_height))

	def update_size(self, screen_width, screen_height):
		temp_dim = min(screen_height, screen_width)
		self.width = 0.9 * temp_dim
		self.height = self.width
		self.set_pos(screen_width, screen_height)

	def set_pos(self, screen_width, screen_height):
		width_gap = (screen_width - self.width) / 2
		height_gap = (screen_height - self.height) / 2
		self.position = (width_gap, height_gap)