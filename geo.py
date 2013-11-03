import math

def dist(p1, p2):
	return sum([p1[i]*p2[i] for i in xrange(len(p1))])**0.5

def angle(from_point, to_point):
	return math.atan2(to_point[1]-from_point[1], to_point[0]-from_point[0])

def shift(from_point, angle, distance):
	return (from_point[0]+distance*math.cos(angle), from_point[1]+distance*math.sin(angle))

def nearest(n, quant):
	if type(n)==tuple:
		return tuple([nearest(x, quant) for x in n])
	else:
		return round(n/quant)*quant

def lerp(v1, v2, x):
	return v1*(1-x) + v2*x

def angle_diff(a1, a2):
	return abs(math.atan2(math.sin(a1-a2), math.cos(a1-a2)))
	