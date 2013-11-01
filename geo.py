import math

def dist(p1, p2):
	return ( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )**0.5

def angle(from_point, to_point):
	return math.atan2(to_point[1]-from_point[1], to_point[0]-from_point[0])

def shift(from_point, angle, distance):
	return (from_point[0]+distance*math.cos(angle), from_point[1]+distance*math.sin(angle))
