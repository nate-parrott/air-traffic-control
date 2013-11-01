import random
from geo import *

def random_airplane_name():
	airlines = ['American', 'United', 'Delta', 'Emirates', 'Southwest', 'JetBlue']
	return airlines[int(random.random()*len(airlines))] + ' ' + str(random.randint(1, 350))

class Plane(object):
	def __init__(self, game):
		self.game = game
		self.fuel = 100 # seconds of fuel
		self.name = random_airplane_name()
		self.objectives = [{"type": "gate"}, {"type": "takeoff", "direction": 90}]
		self.target_states = []
		distance = dist((0,0), (self.game.map['width']/2, self.game.map['width']/2))
		angle = random.random()*math.pi*2
		self.position = shift((self.game.map['width']/2, self.game.map['width']/2), angle, distance)
		self.velocity = shift((0,0), angle+math.pi, 1)
		self.altitude = 10000 * (1 + random.random()*0.1)
	
	def advance(self, dt):
		self.position = (self.position[0]+self.velocity[0]*dt, self.position[1]+self.velocity[1]*dt)
