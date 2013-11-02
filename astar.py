
def select_min(items, fn):
	lowest = items[0]
	lowest_score = fn(lowest)
	for item in items:
		score = fn(item)
		if score < lowest_score:
			lowest = item
			lowest_score = score
	return lowest

def astar(starting_state, transition_fn, heuristic_fn, target_state):
	frontier = [(0, [starting_state])]
	visited_states = set()
	while len(frontier):
		visit = select_min(frontier, lambda (cost, states): cost + heuristic_fn(states[-1]))
		frontier.remove(visit)
		cost, states = visit
		if states[-1] not in visited_states:
			visited_states.add(states[-1])
			if states[-1]==target_state:
				return states
			else:
				for further_cost, further_state in transition_fn(states[-1]):
					frontier.append((cost+further_cost, states+[further_state]))
	return None

if __name__=='__main__':
	def jump(n):
		if n%10==0:
			return [(1, n-1), (1, n+1), (2, n-10), (2, n+10)]
		else:
			return [(1, n-1), (1, n+1)]
	print astar(10, jump, lambda x: abs(x-103), 103)
