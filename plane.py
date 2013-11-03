import random
from geo import *
import map

def pick1(l):
	return l[int(random.random()*len(l))]

def random_airplane_name(game):
	used_names = [plane.name for plane in game.planes]
	airlines = ['American', 'United', 'Delta', 'Emirates', 'Southwest', 'JetBlue']
	while True:
		name = pick1(airlines) + ' ' + str(random.randint(1, 350))
		if name not in used_names:
			return name

class Plane(object):
	def __init__(self, game):
		self.game = game
		self.name = random_airplane_name(game)
		self.objectives = [{"type": "gate"}, {"type": "takeoff", "direction": 90}]
		
		self.path = []
		
		self.target_waypoint = pick1(game.route_map.runways.values())
		self.from_waypoint = pick1(game.route_map.aerials)
		self.to_waypoint = self.next_waypoint()
		self.progress_to_waypoint = 0
	
	def current_pos(self):
		return tuple([self.from_waypoint.position[i]*(1-self.progress_to_waypoint) + self.to_waypoint.position[i]*self.progress_to_waypoint for i in xrange(3)])
	
	def advance(self, dt):
		transition_time = [time for time, to_waypoint in self.from_waypoint.connections if to_waypoint==self.to_waypoint][0]
		self.progress_to_waypoint += dt / transition_time
		if self.progress_to_waypoint >= 1:
			self.from_waypoint = self.to_waypoint
			self.to_waypoint = self.next_waypoint()
			self.progress_to_waypoint = 0
	
	def next_waypoint(self):
		if len(self.path)==0:
			self.path = self.game.route_map.route(self.from_waypoint, self.target_waypoint)
			print self.path
		wp = self.path[0]
		self.path.remove(wp)
		return wp
