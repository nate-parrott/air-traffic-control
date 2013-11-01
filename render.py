import pygame

BACKGROUND_COLOR = (0,0,0)
RUNWAY_COLOR = (100, 0, 0)
TAXIWAY_COLOR = (40, 40, 40)
GATE_COLOR = (160, 140, 140)
TEXT_COLOR = (255, 255, 255)

plane = pygame.image.load('plane.png')

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
	dx = to[0]-start[0]
	dy = to[1]-start[1]
	dist = abs(dx+dy)
	p = start
	while p != to:
		fill_cell(game, p, color)
		p = [p[0]+dx/dist, p[1]+dy/dist]

def render(game):
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
		
