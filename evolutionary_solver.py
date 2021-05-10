import math
from copy import deepcopy
from random import choices, random
import itertools
import json
ALPHA = 2
BETA = 4


def wishes_cost(wishes, solution):
	return sum(
		wishes[student][task]**ALPHA
		for student, tasks in solution.items()
		for task in tasks
	)


def pitches_cost(pitches, solution):
	return 0


def cost(pitches, wishes, solution):
	return (
		wishes_cost(wishes, solution) +
		pitches_cost(pitches, solution)
	)


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


def solve(pitches, wishes, n=100, patience=20, diversity=.2):
	assert n > 1 and patience > 0
	# precomputations to pick best solutions to clone and modify
	keep = int(n*diversity)
	keepidx = list(range(keep))
	cumweightclone = list(itertools.accumulate(range(keep, 0, -1)))
	discard = list(range(keep-1, n))
	# needed to sample wishes randomly
	wishesp = wishes_prob(wishes)
	# the starting solutions
	solutions = random_solutions(wishesp, n)
	p = patience
	best_costs = []
	print("Cost so far:")
	while p > 0:
		# compute the cost of the solutions
		costs = [cost(pitches, wishes, s) for s in solutions]
		# sort the solutions by cost
		costs, solutions = zip(*sorted(zip(costs, solutions), key=lambda cs: cs[0]))
		solutions = list(solutions)
		# update the patience
		if best_costs and best_costs[-1] == costs[0]:
			p -= 1
		else:
			p = patience
		best_costs.append(costs[0])
		print(f"{best_costs[-1]:.2f}", end="\r")
		# replace the worse solutions by modified clones of the best solutions
		clonesidx = choices(keepidx, cum_weights=cumweightclone, k=len(discard))
		for i, cloneidx in zip(discard, clonesidx):
			solutions[i] = random_changes(wishesp, solutions[cloneidx], 1)
	print()
	return solutions[0], best_costs
