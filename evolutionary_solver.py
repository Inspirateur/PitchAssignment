import math
from copy import deepcopy
try:
	from Pyewacket import choices, random
except ImportError:
	print(
		"INFO: Try to install Pyewacket if you can, it can speed up the process. "
		"https://pypi.org/project/Pyewacket/\n"
	)
	from random import choices, random
import itertools
from cost import cost


def wishes_prob(wishes):
	# Turn <student, <task, rank>> into <student, (tasks, cumweights)>
	res = {}
	for student, ranking in wishes.items():
		probs = list(itertools.accumulate(math.exp(1-v) for v in ranking.values()))
		res[student] = (list(ranking.keys()), probs)
	return res


def random_wish(tasks, cumweights):
	return choices(tasks, cum_weights=cumweights)[0]


def random_solutions(wishesp, n):
	return [
		{
			student: [random_wish(*wishesp[student])]
			for student in wishesp
		}
		for _ in range(n)
	]


def random_changes(wishesp, solution, k):
	res = deepcopy(solution)
	students = choices(list(wishesp.keys()), k=k)
	for student in students:
		newtask = random_wish(*wishesp[student])
		if newtask != res[student][0]:
			if random() < .8:
				# just change a task
				res[student][0] = newtask
			else:
				# add/remove a task
				if len(res[student]) == 1:
					res[student].append(newtask)
				else:
					del res[student][-1]
	return res


def solve(pitches, wishes, n=1000, patience=30, diversity=.5):
	# FIXME: if author of pitch A ends up on another pitch, the role he picked on pitch A should be available to fill
	# FIXME: allow students to chose to work on only 1 project
	assert n > 1 and patience > 0
	# precomputations to pick best solutions to clone and modify
	keep = int(n*diversity)
	keepidx = list(range(keep))
	discard = list(range(keep-1, n))
	# needed to sample wishes randomly
	wishesp = wishes_prob(wishes)
	# the starting solutions
	solutions = random_solutions(wishesp, n)
	p = patience
	best_costs = []
	alpha = 3
	beta = 1
	print("Cost so far:")
	while p > 0:
		# compute the cost of the solutions
		costs = [cost(pitches, wishes, s, alpha, beta) for s in solutions]
		# sort the solutions by cost
		costs, solutions = zip(*sorted(zip(costs, solutions), key=lambda cs: cs[0]))
		solutions = list(solutions)
		# update the patience
		if best_costs and best_costs[-1] == costs[0]:
			p -= 1
		else:
			p = patience
		best_costs.append(costs[0])
		print(f"{best_costs[-1]:.2f}  (p={int(p/10)}) ", end="\r")
		# replace the worse solutions by modified clones of the best solutions
		clonesidx = choices(keepidx, k=len(discard))
		for i, cloneidx in zip(discard, clonesidx):
			solutions[i] = random_changes(wishesp, solutions[cloneidx], 2)
	print()
	return solutions[0], best_costs
