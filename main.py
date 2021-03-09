import json
import random


with open("students.json", "r") as fstudents:
	# <role, [students]>
	students: dict = json.load(fstudents)


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


def shuffle_extend(elems, n):
	# shuffle and extends elems such that len(elems) >= n
	elems = random.sample(elems, len(elems))
	i = 0
	while len(elems) < n:
		elems.append(elems[i])
		i += 1
	return elems


def solve():
	with open("wishes.csv", "r") as fwishes:
		pitches = fwishes.readline().strip().split(", ")[1:]
		wishes = {}
		for line in fwishes:
			student, *scores = line.strip().split(", ")
			wishes[student] = scores

	def fav_pitch(r, s):
		return max(
			filter(
				lambda ps: ps[0] in res and r not in res[ps[0]],
				zip(pitches, wishes[s])
			),
			key=lambda ps: ps[1]
		)[0]

	def least_staffed():
		return min(
			res.items(),
			key=lambda p_staff: len(p_staff[1])
		)[0]

	# <pitch, {role: student}>
	res = {pitch: {} for pitch in pitches}

	# for now, we'll retain as many pitches as there is prog students
	amount = len(students["Prog"])
	assert len(pitches) >= amount
	while True:
		# assign the students to the remaining pitches
		for role, group in students.items():
			group = shuffle_extend(group, amount)
			for student in group:
				pitch = fav_pitch(role, student)
				res[pitch][role] = student
		if len(res) == amount:
			break
		pitch = least_staffed()
		del res[pitch]
		# reset the staff on every pitch
		res = {pitch: {} for pitch in res}

	# display the results
	pmap = {pitch: i for i, pitch in enumerate(pitches)}

	def get_score(s, p):
		return wishes[s][pmap[p]]

	for pitch, staff in res.items():
		print(pitch)
		for role, student in staff.items():
			print(f"  - {role}: {student} ({get_score(student, pitch)})")
	return res


if __name__ == '__main__':
	# generate_wishes()
	solve()
