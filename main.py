from collections import defaultdict
import json
from evolutionary_solver import solve
import cProfile


def filter_author_roles(pitches, wishes):
	# make sure that any (pitch, role) present in the pitch author's wishes are exclusive,
	# ie the pitch author has priority on any role he wants
	locked = {}
	for pitch1 in pitches:
		author = pitches[pitch1]["author"]
		for pitch2, role in wishes[author]:
			if pitch1 == pitch2:
				locked[(pitch1, role)] = author
	res = {}
	for student in wishes:
		res[student] = list(filter(
			lambda wish: wish not in locked or locked[wish] == student,
			wishes[student]
		))
	return res


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
	workers = defaultdict(lambda: defaultdict(list))
	for student, tasks in solution.items():
		for pitch, role in tasks:
			name = "*"+student if student == pitches[pitch]["author"] else student
			workers[pitch][role].append(f"{name} {wishes[student][(pitch, role)]}")
	for pitch in workers:
		print(pitch)
		for role, students in workers[pitch].items():
			print(f"\t{role} ({pitches[pitch]['workload'][role]}):", ", ".join(students))
		print()


def main():
	with open("dummy_pitches.json", "r") as fpitches:
		pitches = json.load(fpitches)
	with open("dummy_wishes.json", "r") as fwishes:
		wishes = json.load(fwishes)
		# reconvert the tuples that got converted to list with json
		for student, ranking in wishes.items():
			wishes[student] = [(pitch, role) for pitch, role in ranking]
	wishes = normdict_wishes(filter_author_roles(pitches, wishes))
	for _ in range(8):
		solution = solve(pitches, wishes)
		print_solution(pitches, wishes, solution)


if __name__ == "__main__":
	main()
