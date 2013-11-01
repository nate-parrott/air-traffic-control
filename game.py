import pygame
import render

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
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					break
			render.render(self)
			pygame.display.update()
			self.clock.tick(30)
		pygame.quit()

if __name__=='__main__':
	import json
	map = json.loads(open('map1.json').read())
	Game(map).run()
