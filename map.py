
def cells_between(start, to):
	yield start
	dx = to[0]-start[0]
	dy = to[1]-start[1]
	dist = abs(dx+dy)
	p = start
	while p != to:
		p = [p[0]+dx/dist, p[1]+dy/dist]
		yield p

def feature_at_pos(map, pos):
	pos = list(pos)
	for feature in map['features']:
		if 'position' in feature and pos == feature['position']:
			return feature
		elif 'start' in feature and pos in list(cells_between(feature['start'], feature['end'])):
			return feature
	return None

