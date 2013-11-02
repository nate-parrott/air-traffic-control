import random
from geo import *
import map

def random_airplane_name():
	airlines = ['American', 'United', 'Delta', 'Emirates', 'Southwest', 'JetBlue']
	return airlines[int(random.random()*len(airlines))] + ' ' + str(random.randint(1, 350))

class Plane(object):
	def __init__(self, game):
		self.game = game
		self.fuel = 100.0 # seconds of fuel
		self.name = random_airplane_name()
		self.objectives = [{"type": "gate"}, {"type": "takeoff", "direction": 90}]
		
		self.target_state = State()
		self.target_state.position = (5,5)
		self.target_state.velocity = (0,0)
		self.target_state.altitude = 0
		
		self.from_state = random_state(game)
		self.to_state = self.from_state
		self.path = []
		self.state_transition_duration = 1
		self.time_left_in_state_transition = -1
	
	def current_state(self):
		return self.from_state.interpolate(self.to_state, 1-self.time_left_in_state_transition/self.state_transition_duration)
	
	def advance(self, dt):
		self.time_left_in_state_transition -= dt
		if self.time_left_in_state_transition < 0:
			self.from_state = self.to_state
			self.to_state = self.next_state()
			self.time_left_in_state_transition = self.state_transition_duration
		self.fuel -= dt
	
	def next_state(self):
		if len(self.path)==0:
			self.path = self.calculate_path()
		n = self.path[0]
		self.path.remove(n)
		return n
	
	def calculate_path(self):
		target = self.target_state
		path = astar.astar(
			tuple_from_state(self.from_state), 
			lambda state: state_transitions(self, state, self.state_transition_duration), 
			lambda state_tuple: state_from_tuple(state_tuple).difference(target), 
			tuple_from_state(target))
		return [state_from_tuple(state_tuple) for state_tuple in path]

def state_transitions(plane, state_tuple, dt):
	print state_tuple
	state = state_from_tuple(state_tuple)
	
	for alt_delta in (-1, 0, 1):
		for vx_delta in (-1, 0, 1):
			for vy_delta in (-1, 0, 1):
				new_state = State()
				new_state.altitude = state.altitude + alt_delta
				new_state.velocity = (state.velocity[0] + vx_delta, state.velocity[1] + vy_delta)
				new_state.position = (state.position[0] + state.velocity[0], state.position[1] + state.velocity[1])
				if new_state.is_valid(plane.game):
					yield state.difference(new_state), tuple_from_state(new_state)
	

"""
def state_transitions(plane, state_tuple, dt):
	print state_tuple
	state = state_from_tuple(state_tuple)
	
	over_feature = map.feature_at_pos(plane.game.map, state.position)
	
	speed = dist(state.velocity, (0,0))
	direction = angle((0,0), state.velocity)
	
	new_altitudes = [state.altitude]
	if state.altitude==0:
		if speed >= 1.5:
			new_altitudes.append(20*dt)
	else:
		new_altitudes += [state.altitude+70*dt, max(0, state.altitude-70*dt)]
	
	new_speeds = [speed, speed-1*dt, speed+1*dt]
	new_speeds = [spd for spd in new_speeds if spd >= 0]
	
	new_directions = [direction, direction+math.pi*2*0.1*dt, direction-math.pi*2*0.1*dt]
	
	for alt in new_altitudes:
		for speed in new_speeds:
			for direction in new_directions:
				new_state = State()
				
				new_state.velocity = shift((0,0), direction, speed)
				new_state.position = (state.position[0] + new_state.velocity[0], state.position[1] + new_state.velocity[1])
				new_state.altitude = alt
				
				if new_state.is_valid():
					new_state.position = nearest(new_state.position, 0.5)
					new_state.velocity = nearest(new_state.velocity, 0.2)
					new_state.altitude = nearest(new_state.altitude, 20)
					if new_state.close_to(plane.target_state):
						yield state.difference(plane.target_state), tuple_from_state(plane.target_state)
					else:
						yield state.difference(new_state), tuple_from_state(new_state)

"""