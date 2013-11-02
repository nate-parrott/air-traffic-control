import astar

def random_state(game):	
	s = State()
	distance = dist((0,0), (game.map['width']/2, game.map['height']/2))
	angle = random.random()*math.pi*2
	s.position = nearest(shift((game.map['width']/2, game.map['height']/2), angle, distance), 1)
	s.velocity = nearest(shift((0,0), angle+math.pi, 4), 1)
	s.altitude = 3
	return s

class State(object):
	position = (0,0)
	velocity = (0,0)
	altitude = 0
	
	def interpolate(self, other, x):
		s = State()
		s.position = (lerp(self.position[0], other.position[0], x), lerp(self.position[1], other.position[1], x))
		s.velocity = (lerp(self.velocity[0], other.velocity[0], x), lerp(self.velocity[1], other.velocity[1], x))
		s.altitude = lerp(self.altitude, other.altitude, x)
		return s
	
	def is_valid(self, game):
		over_feature = map.feature_at_pos(game.map, self.position)
		
		fast_enough = dist((0,0), self.velocity) >= 3 or self.altitude == 0
		above_ground = self.altitude > 0
		on_ground = (not above_ground) and over_feature != None
		return fast_enough and (above_ground or on_ground)
	
	def close_to(self, target_state):
		return (abs(target_state.altitude - self.altitude) <= 50 
			and dist(target_state.position, self.position) < 0.3 
			and dist(target_state.velocity, self.velocity) < 0.3)
	
	def difference(self, other_state):
		return dist(self.position, other_state.position) + dist(self.velocity, other_state.velocity) + abs(self.altitude - other_state.altitude)

def state_from_tuple(tp):
	s = State()
	s.position, s.velocity, s.altitude = tp
	return s

def tuple_from_state(s):
	return (s.position, s.velocity, s.altitude)
