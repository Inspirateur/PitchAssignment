from collections import defaultdict
from copy import copy
import math
try:
	from Pyewacket import choices, random, sample
except ImportError:
	print(
		"INFO: Try to install Pyewacket if you can, it can speed up the process.\n"
		"https://pypi.org/project/Pyewacket/\n"
	)
	from random import choices, random, sample
import itertools
from time import time
from cost import cost
from logger import log


def wishes_prob(wishes):
	"""
	Turn <student, <task, rank>> into <student, (tasks, cumweights)>
	so that we can sample random tasks from it
	(higher ranking tasks have greater prob of being picked)
	:param wishes: <student, <task, rank>>
	:return: <student, (tasks, cumweights)>
	"""
	res = {}
	for student, ranking in wishes.items():
		cumweights = list(itertools.accumulate(math.exp(1-v) for v in ranking.values()))
		res[student] = (list(ranking.keys()), cumweights)
	return res


def random_task(tasks, cumweights):
	# (pitch, role)
	return choices(tasks, cum_weights=cumweights)[0]


def random_solutions(wishesp, n):
	return [
		{
			(student, *random_task(*wishesp[student]))
			for student in wishesp
		}
		for _ in range(n)
	]


def student_tasks(solution, student1):
	studenttasks = 0
	for student2, _, _ in solution:
		if student2 == student1:
			studenttasks += 1
	return studenttasks


def random_changes(wishesp, solution, k):
	tasks = sample(solution, k=k)
	for (student, pitch, role) in tasks:
		newtask = (student, *random_task(*wishesp[student]))
		if random() < .8:
			# just change a task
			solution.add(newtask)
			solution.remove((student, pitch, role))
		else:
			# add/remove a task
			if student_tasks(solution, student) == 1:
				solution.add(newtask)
			else:
				solution.remove((student, pitch, role))


def unique_pitches(solutions):
	return len(
		{
			tuple(sorted(list({
				pitch
				for _, pitch, _ in solution
			})))
			for solution in solutions
		}
	)


def solve(pitches, wishes, n=1000, patience=200, diversity=.90):
	# FIXME: allow students to chose to work on only 1 project
	assert n > 1 and patience > 0
	# precomputations to pick best solutions to clone and modify
	keep = int(n*diversity)
	discard = list(range(keep-1, n))
	# needed to sample wishes randomly
	wishesp = wishes_prob(wishes)
	# the starting solutions [(student, pitch, role)]
	solutions = random_solutions(wishesp, n)
	p = patience
	# for printing in the console with padded 0
	zfill_p = len(str(patience))-1
	best_costs = []
	unq_pitches = []
	costs = []
	alpha = 3
	beta = 1
	print("Cost so far:")
	start = time()
	count = 0
	while p > 0:
		count += 1
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
		unq_pitches.append(unique_pitches(solutions))
		print(f"{best_costs[-1]:.2f}  (p={str(int(p/10)).zfill(zfill_p)}) ", end="\r")
		# replace the worse solutions by modified clones of the best solutions
		for i in discard:
			solutions[i] = copy(solutions[i % keep])
			random_changes(wishesp, solutions[i], 2)
	print()
	delta = time()-start
	print(f"in {delta:,.1f} sec - {1000*delta/count:.1f}ms/it")
	log("best_costs", best_costs)
	log("unique_pitches", unq_pitches)
	log("final_costs", costs)
	# [(student, pitch, role)]
	best = solutions[0]
	# turn into <student, [(pitch, role)]>
	res = defaultdict(list)
	for student, pitch, role in best:
		res[student].append((pitch, role))
	return res
