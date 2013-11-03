import pygame
import math
import map

BACKGROUND_COLOR = (0,0,0)
RUNWAY_COLOR = (100, 0, 0)
TAXIWAY_COLOR = (40, 40, 40)
GATE_COLOR = (160, 140, 140)
TEXT_COLOR = (255, 255, 255)

plane_image = pygame.image.load('plane.png')

def draw_name(game, point, text):
	xsize = game.w / game.map['width']
	ysize = game.h / game.map['height']
	size = int(min(xsize, ysize)*0.6)
	font = pygame.font.Font('courier-new-bold.ttf', size)
	rendered = font.render(text, True, TEXT_COLOR)
	game.surface.blit(rendered, (point[0]*xsize, point[1]*ysize))

def fill_cell(game, point, color):
	xsize = game.w / game.map['width']
	ysize = game.h / game.map['height']
	pygame.draw.rect(game.surface, color, (xsize*point[0], ysize*point[1], xsize, ysize))

def draw_path(game, start, to, color):
	for cell in map.cells_between(start, to):
		fill_cell(game, cell, color)

def render(game):
	xsize = game.w / game.map['width']
	ysize = game.h / game.map['height']
	
	game.surface.fill(BACKGROUND_COLOR)
	for feature in game.map['features']:
		t = feature['type']
		if t=='runway':
			draw_path(game, feature['start'], feature['end'], RUNWAY_COLOR)
			fill_cell(game, feature['start'], [int(c*1.5) for c in RUNWAY_COLOR])
			draw_name(game, feature['start'], feature['name'])
		elif t=='taxiway':
			draw_path(game, feature['start'], feature['end'], TAXIWAY_COLOR)
			center = [int((feature['start'][0]+feature['end'][0])/2), int((feature['start'][1]+feature['end'][1])/2)]
			draw_name(game, center, feature['name'])
		elif t=='gate':
			fill_cell(game, feature['position'], GATE_COLOR)
			draw_name(game, feature['position'], feature['name'])
	
	size = (xsize + ysize)/2 * 0.8
	scale = (size / plane_image.get_width() + size / plane_image.get_height())/2.0
	for plane in game.planes:
		position = plane.current_pos()
		angle = 0#math.atan2(state.velocity[1], state.velocity[0]) * 180 / math.pi
		transformed = pygame.transform.rotozoom(plane_image, -angle, scale)
		game.surface.blit(transformed, ((position[0]+0.5)*xsize-transformed.get_width()/2, (position[1]+0.5)*ysize-transformed.get_height()/2))
		font = pygame.font.Font("courier-new-bold.ttf", 13)
		text_pos = (position[0]*xsize-transformed.get_width()/2, position[1]*ysize+transformed.get_height()/2)
		plane_label = "%s [%i ft]"%(plane.name, position[2])
		game.surface.blit(font.render(plane_label, True, TEXT_COLOR), text_pos)

