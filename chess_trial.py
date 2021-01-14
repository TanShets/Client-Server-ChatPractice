import pygame as pg
from Grid import Grid
from piece import *
import client as cli
import sys

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

def receive_move():
	global turn
	global pieces
	global grid
	global isEnd
	if isEnd:
		sys.exit()
	move = cli.client.recv(2048).decode(cli.FORMAT)
	print(move)
	if len(move) >= 4:
		move = move[:4]
		print(move)
		a1, b1, a2, b2 = move[0], move[1], move[2], move[3]
		x1, y1 = grid.pos[a1], grid.pos[int(b1)]
		x2, y2 = grid.pos[a2], grid.pos[int(b2)]
		if pieces.get((x1, y1), False):
			temp_piece = pieces[(x1, y1)]
			temp_piece.set_position((x2, y2))
			pieces[(x2, y2)] = temp_piece
			del pieces[(x1, y1)]
			turn = True

def draw():
	global window, grid, screen_width, screen_height, pieces
	if(screen_width != pg.display.get_surface().get_width() or screen_height != pg.display.get_surface().get_height()):
		change_scale()
	
	window.blit(bg, (0,0))
	grid.draw(window)
	for i in pieces.keys():
		pieces[i].draw(window, grid)
	pg.display.update()

def change_scale():
	global window
	global grid
	global bg
	global bg_og
	window = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
	#print(screen_width, screen_height)
	grid.update_size(screen_width, screen_height)
	for i in pieces.keys():
		pieces[i].change_scale(grid.square_side)
	bg = pg.transform.scale(bg_og, (screen_width, screen_height))

pg.init()
window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.RESIZABLE)
pg.display.set_caption("Chess")

bg_og = pg.image.load('assets/background.jpeg')
bg = pg.transform.scale(bg_og, (WINDOW_WIDTH, WINDOW_HEIGHT))
run = True
screen_width, screen_height = WINDOW_WIDTH, WINDOW_HEIGHT

isWhite = True
while cli.assigned_id == None:
	pass
if cli.assigned_id % 2 == 0:
	isWhite = False
grid = Grid(screen_width, screen_height, 400, isWhite, black = (34, 67, 45))

if isWhite:
	turn = True
else:
	turn = False
pieces = setup(isWhite, grid)
'''
for i in pieces.keys():
	print(i,":", pieces[i].name)
'''
print(grid.square_side)
hasClicked = False
square_pos = None
selected_piece = None
move_set = None
isEnd = False
#window.blit(bg, (0,0))
while run:
	window.fill((0,0,0))
	pg.time.delay(100)

	draw()
	#print(pg.display.get_surface().get_size())

	for event in pg.event.get():
		if event.type == pg.QUIT:
			isEnd = True
			run = False
		elif event.type == pg.VIDEORESIZE:
			screen_width = event.w
			screen_height = event.h
		elif event.type == pg.MOUSEBUTTONUP:
			square_pos = grid.get_cursor_square(pg.mouse.get_pos())
			if pieces.get(square_pos, False):
				print("Found piece")
				selected_piece = pieces[square_pos]
				move_set = selected_piece.get_moveset(pieces)
			else:
				print("No piece here")
				if selected_piece != None:
					if move_set != None and square_pos in move_set and turn:
						print("Success")
						temp_pos = selected_piece.position
						selected_piece.set_position(square_pos)
						pieces[square_pos] = selected_piece

						x1, y1 = grid.op_pos_x[temp_pos[0]], grid.op_pos_y[temp_pos[1]]
						x2, y2 = grid.op_pos_x[square_pos[0]], grid.op_pos_y[square_pos[1]]

						message = str(x1) + str(y1) + str(x2) + str(y2)
						cli.send_message(message, cli.client)
						turn = False

						del pieces[temp_pos]
						del temp_pos
						selected_piece = None
						move_set = None
					else:
						print("NO")
				else:
					print("Non")
			print(grid.get_cursor_square(pg.mouse.get_pos()))

	if not turn:
		#print("HEre")
		thread = cli.threading.Thread(target = receive_move, args = ())
		thread.start()
pg.quit()
cli.send_message("exit", cli.client)
cli.client.close()