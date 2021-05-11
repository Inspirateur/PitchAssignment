from collections import defaultdict


def wishes_cost(wishes, solution):
	return sum(
		wishes[student][task]**3
		for student, tasks in solution.items()
		for task in tasks
	)


def workload_diff(target, proposed):
	total = 0
	for role in target:
		if role not in proposed:
			# an unfulfilled role cost twice as much
			diff = 2*target[role]
		else:
			diff = target[role]-proposed[role]
			# an excess of work on a role costs half as a lack of work
			if diff < 0:
				diff = abs(diff)/2
		total += diff
	return total


def pitches_cost(pitches, solution):
	workloads = defaultdict(lambda: defaultdict(float))
	for student, tasks in solution.items():
		for pitch, role in tasks:
			workloads[pitch][role] += 1/len(tasks)
	return sum(
		workload_diff(pitches[pitch]["workload"], workloads[pitch])
		for pitch in pitches
		if pitch in workloads
	)


def cost(pitches, wishes, solution, alpha=3, beta=1):
	return (
		alpha*wishes_cost(wishes, solution) +
		beta*pitches_cost(pitches, solution)
	)/(alpha+beta)
