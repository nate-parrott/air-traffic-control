import pygame
import render
import plane as plane
import random
import routing

FRAME_RATE = 30

NEW_PLANES_PER_SECOND = 0 # 0.1

class Game(object):
	def __init__(self, map):
		self.map = map
		self.route_map = routing.RouteMap(map)
	
	def run(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		aspect = self.map['width']*1.0/self.map['height']
		self.w = 700
		self.h = int(self.w/aspect)
		self.surface = pygame.display.set_mode((self.w, self.h))
		self.planes = []
		self.planes.append(plane.Plane(self))
		while True:
			dt = 1.0/FRAME_RATE
			# handle events:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					break
			# make new planes:
			if random.random() < dt * NEW_PLANES_PER_SECOND:
				self.planes.append(plane.Plane(self))
			# update existing planes:
			for p in self.planes:
				p.advance(dt)
			# render graphics:
			render.render(self)
			pygame.display.update()
			self.clock.tick(FRAME_RATE)
		pygame.quit()

if __name__=='__main__':
	import json
	map = json.loads(open('map1.json').read())
	Game(map).run()
