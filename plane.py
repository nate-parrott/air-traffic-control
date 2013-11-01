

class Plane(object):
	def __init__(self):
		self.fuel = 100 # seconds of fuel
		self.objectives = [{"type": "gate"}, {"type": "takeoff", "direction": 90}]
		
