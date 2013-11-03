import astar
import map
from geo import *
import math

TAXI_SPEED = 1.0
AIR_SPEED = 3.0

AIR_TURN_RADIANS_PER_UNIT = math.pi * 0.2
ALTITUDE_DELTA_PER_UNIT = 0.4

def random_state(game):	
	s = State()
	distance = dist((0,0), (game.map['width']/2, game.map['height']/2))
	angle = random.random()*math.pi*2
	s.position = nearest(shift((game.map['width']/2, game.map['height']/2), angle, distance), 1)
	s.velocity = nearest(shift((0,0), angle+math.pi, 4), 1)
	s.altitude = 3
	return s

class Waypoint(object):
	def __init__(self, position):
		self.position = position
		self.connections = [] # tuples of (time, other_waypoint)
		self.direction = None
	
	def distance(self, other):
		return dist(self.position, other.position)
	
	def heuristic(self, other):
		return self.distance(other) / AIR_SPEED
	
	def __repr__(self):
		return "<%s, %s, %i connections>"%(self.position, '-' if self.direction==None else str(self.direction), len(self.connections))

class RouteMap(object):
	def __init__(self, amap):
		runway_start_waypoints = {}
		taxiable_waypoints = []
		gate_waypoints = {}
		aerial_waypoints = []
	
		for feature in amap['features']:
			if feature['type']=='runway':
				runway_start = Waypoint((feature['start'][0], feature['start'][1], 0))
				runway_start_waypoints[feature['name']] = runway_start
				taxiable_waypoints.append(runway_start)
			
				takeoff_speed = dist(feature['start'], feature['end']) / ((AIR_SPEED + TAXI_SPEED)/2)
			
				runway_incoming = Waypoint((feature['end'][0], feature['end'][1], 1))
				runway_incoming.connections.append((takeoff_speed, runway_start))
				runway_incoming.direction = angle(feature['end'], feature['start'])
				aerial_waypoints.append(runway_incoming)
			
				runway_outgoing = Waypoint((feature['end'][0], feature['end'][1], 1))
				runway_start.connections.append((takeoff_speed, runway_outgoing))
				runway_outgoing.direction = runway_incoming.direction + math.pi
				aerial_waypoints.append(runway_outgoing)
			
			elif feature['type']=='taxiway' or feature['type']=='gate':
				cells = map.cells_between(feature['start'], feature['end']) if 'start' in feature else [feature['position']]
				for cell in cells:
					wp = Waypoint((cell[0], cell[1], 0))
					taxiable_waypoints.append(wp)
					if feature['type']=='gate':
						gate_waypoints[feature['name']] = wp
	
		# connect all adjacent taxiable waypoints:
		for wp in taxiable_waypoints:
			for other_wp in taxiable_waypoints:
				if dist(wp.position, other_wp.position) <= dist((0,0), (1,1)):
					wp.connections.append((1/TAXI_SPEED, other_wp))
	
		air_grid_dist = 5
		directions = [0, math.pi*0.5, math.pi, math.pi*1.5]
		altitudes = [1]
		for x in xrange(0, amap['width'], air_grid_dist):
			for y in xrange(0, amap['height'], air_grid_dist):
				for alt in altitudes:
					for direction in directions:
						wp = Waypoint((x, y, alt))
						wp.direction = direction
						aerial_waypoints.append(wp)
	
		# connect all appropriate aerial waypoints:
		for wp in aerial_waypoints:
			for other_wp in aerial_waypoints:
				if wp==other_wp: continue
				
				d = dist(wp.position[:2], other_wp.position[:2])
				#wp.connections.append((d / AIR_SPEED, other_wp))
				if d>0 and angle_diff(wp.direction, other_wp.direction) <= AIR_TURN_RADIANS_PER_UNIT * d and abs(wp.position[2] - other_wp.position[2]) <= ALTITUDE_DELTA_PER_UNIT * d and angle_diff(wp.direction, angle(wp.position[:2], other_wp.position[:2])) <= math.pi/2:
					wp.connections.append((d / AIR_SPEED, other_wp))
		
		self.aerials = aerial_waypoints
		self.runways = runway_start_waypoints
		self.gates = gate_waypoints
	
	def route(self, from_waypoint, to_waypoint):
		#print 'Routing from', from_waypoint, 'to', to_waypoint
		return astar.astar(
			from_waypoint,
			lambda wp: wp.connections,
			lambda wp: wp.heuristic(to_waypoint),
			to_waypoint
		)
