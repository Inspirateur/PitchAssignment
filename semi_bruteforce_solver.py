from collections import deque


def score_pitches(pitches, wishes):
	"""
	Naively score pitches by assigning them the best possible team
	and counting the total wish score
	:param pitches: <pitch, <role, load>>
	:param wishes: <student, [(pitch, role)]>
	:return: (pitches, scores) sorted by ascending score
	"""
	best_teams = {
		pitch: {role: deque([float("+inf")]*load, maxlen=load) for role, load in loads}
		for pitch, loads in pitches.items()
	}
	for student, tasks in wishes.items():
		for rank, (pitch, role) in enumerate(tasks):
			if rank < best_teams[pitch][role][-1]:
				best_teams[pitch][role].append(rank)
	return zip(*sorted([
		(pitch, sum(sum(ranks) for ranks in workers.value()))
		for pitch, workers in best_teams
	], key=lambda ps: ps[1]))


def bruteforce(pitches, wishes):
	"""
	Minimizes the cost on a selection of pitches by bruteforce
	:param pitches: <pitch, <role, load>>
	:param wishes: <student, [(pitch, role)]>
	:return: <pitch, <role, [student]>>
	"""
	...


def solve(pitches, wishes):
	"""
	Attempt to minimise the cost function with a naive evolutionnary solver
	:param pitches: <pitch, <role, load>>
	:param wishes: <student, [(pitch, role)]>
	:return: <pitch, <role, [student]>>
	"""
	pitches, _ = score_pitches(pitches, wishes)
	load = 0
	selected_pitches = []
	for pitch, loads in pitches.items():
		p_load = sum(loads.values())
		new_load = load + p_load
		if abs(len(wishes)-new_load) < abs(len(wishes)-load):
			load = new_load
			selected_pitches.append(pitch)
		else:
			break
	return bruteforce(
		{pitch: pitches[pitch] for pitch in selected_pitches},
		wishes
	)
