import pygame

class Game(object):
	def __init__(self, map):
		self.map = map
	
	def run(self):
		

if __name__=='__main__':
	import json
	map = json.loads(open('map1.json').read())
	Game(map).run()
