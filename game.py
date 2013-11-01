import pygame

class Game(object):
	def __init__(self, map):
		self.map = map
	
	def run(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		aspect = self.map['width']*1.0/self.map['height']
		self.w = 700
		self.h = int(self.w/aspect)
		self.surface = pygame.display.set_mode((self.w, self.h))
		while True:
			self.surface.fill(pygame.Color(255, 255, 255))
			pygame.display.update()
			self.clock.tick(30)

if __name__=='__main__':
	import json
	map = json.loads(open('map1.json').read())
	Game(map).run()
