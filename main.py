from collections import defaultdict
import json
from evolutionary_solver import solve
import cProfile


def normdict_wishes(wishes):
	# Normalize ranks with max=1 and turns them into a dict
	res = {}
	for student, ranking in wishes.items():
		res[student] = {
			task: (i + 1)/len(ranking)
			for i, task in enumerate(ranking)
		}
	return res


def pretty_wishes(wishes):
	res = {}
	for student, ranking in wishes.items():
		res[student] = {
			task: f"{i+1}/{len(ranking)}"
			for i, task in enumerate(ranking)
		}
	return res


def print_solution(pitches, wishes, solution):
	wishes = pretty_wishes(wishes)
	workers = {}
	for student, tasks in solution.items():
		for pitch, role in tasks:
			name = student
			if pitch not in workers:
				workers[pitch] = {
					role: [] for role in pitches[pitch]["workload"]
				}
			workers[pitch][role].append(f"{name} {wishes[student][(pitch, role)]}")
	for pitch in workers:
		print(f"{pitch} ({pitches[pitch]['author']})")
		for role, students in workers[pitch].items():
			print(f"\t{role} ({pitches[pitch]['workload'][role]}):", ", ".join(students))
		print()


def main():
	with open("dummy_pitches.json", "r") as fpitches:
		# pitches[pitch]["workload"]: <role, load>
		# pitches[pitch]["author"]: a student
		pitches = json.load(fpitches)
	with open("dummy_wishes.json", "r") as fwishes:
		# <student, [pitch, role]>
		wishes = json.load(fwishes)
		# reconvert the tuples that got converted to list with json
		for student, ranking in wishes.items():
			wishes[student] = [(pitch, role) for pitch, role in ranking]
	wishes = normdict_wishes(wishes)
	for _ in range(4):
		solution = solve(pitches, wishes)
		print_solution(pitches, wishes, solution)


if __name__ == "__main__":
	main()
