from collections import deque
import itertools
import json
import random
import sys
from tqdm import tqdm


def shuffle_extend(elems, amount):
	# shuffle and extends elems such that len(elems) >= n
	elems = random.sample(elems, len(elems))
	i = 0
	while len(elems) < amount:
		elems.append(elems[i])
		i += 1
	return elems


with open("students.json", "r") as fstudents:
	# <role, [students]>
	students: dict = json.load(fstudents)
	# we'll retain as many pitches as there is prog students
	n = len(students["Prog"])
	for _role in students:
		students[_role] = shuffle_extend(students[_role], n)


def generate_wishes():
	# make fake pitches and random wishes to test the algorithm
	pitches = [
		"Minecraft but better", "Croissant Crush", "Basketball Physics",
		"Doki doki Chess Club", "Pokimon Autobattler", "Sound Racer",
		"Dark Sels", "Covid: Isolation", "Bioshocolatine"
	]
	student_list = sum(students.values(), [])
	with open("wishes.csv", "w") as fwishes:
		# write the csv header
		fwishes.write("students, " + ", ".join(pitches) + "\n")
		for student in student_list:
			fwishes.write(student + ", ")
			scores = [str(random.randint(1, 7)) for _ in pitches]
			fwishes.write(", ".join(scores) + "\n")


def gale_shapley(pitches, wishes):
	"""
	:param pitches: [pitch idx] a subset of all pitches (specified by index)
	:param wishes: <student, [pitch idx]> ranked by preference
	:return: <pitch idx, <role, (student, rank)>> a solution
	"""
	# <pitch idx, <role: (student, rank)>>
	res = {pitch: {} for pitch in pitches}
	for role in students:
		to_assign = deque(students[role])
		while to_assign:
			a = to_assign.popleft()
			for i, pitch in enumerate(wishes[a]):
				if pitch in res:
					if role not in res[pitch]:
						res[pitch][role] = (a, i)
						break
					b, r = res[pitch][role]
					if i < r:
						res[pitch][role] = (a, i)
						to_assign.append(b)
						break
	return res


def score(solution):
	return sum(
		rank+1
		for staff in solution.values()
		for _, rank in staff.values()
	)


def solve():
	with open("wishes.csv", "r") as fwishes:
		pitches = fwishes.readline().strip().split(", ")[1:]
		# <student, [pitches idx]> ranked by preference
		wishes = {}
		for line in fwishes:
			student, *scores = line.strip().split(", ")
			wishes[student] = sorted(range(len(scores)), key=scores.__getitem__, reverse=True)

	min_score = float("+inf")
	best = None
	for sub_pitches in tqdm(
			itertools.combinations(range(len(pitches)), n), desc="Brutefoce", file=sys.stdout
	):
		res = gale_shapley(sub_pitches, wishes)
		new_score = score(res)
		if new_score < min_score:
			min_score = new_score
			best = res

	# display the results
	for pitch, staff in best.items():
		print(pitches[pitch])
		for role, (student, rank) in staff.items():
			print(f"  - {role}: {student} ({rank+1})")
		print()
	print("Total score:", min_score)
	return best


if __name__ == '__main__':
	# generate_wishes()
	solve()
