import pygame as pg
import Grid
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

def change_scale():
	global window
	global grid
	global bg
	global bg_og
	window = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
	#print(screen_width, screen_height)
	grid.update_size(screen_width, screen_height)
	bg = pg.transform.scale(bg_og, (screen_width, screen_height))

pg.init()
window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.RESIZABLE)
pg.display.set_caption("Chess")

bg_og = pg.image.load('assets/background.jpeg')
bg = pg.transform.scale(bg_og, (WINDOW_WIDTH, WINDOW_HEIGHT))
run = True
screen_width, screen_height = WINDOW_WIDTH, WINDOW_HEIGHT
grid = Grid(screen_width, screen_height, 400, True, black = (34, 67, 45))
#window.blit(bg, (0,0))
while run:
	window.fill((0,0,0))
	pg.time.delay(100)
	print(pg.display.get_surface().get_size())
	if(screen_width != pg.display.get_surface().get_width() or screen_height != pg.display.get_surface().get_height()):
		change_scale()
	window.blit(bg, (0,0))
	grid.draw(window)
	pg.draw.rect(window, (100, 50, 10), (25, 25, 20, 20))
	pg.display.update()

	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False
		elif event.type == pg.VIDEORESIZE:
			screen_width = event.w
			screen_height = event.h
pg.quit()