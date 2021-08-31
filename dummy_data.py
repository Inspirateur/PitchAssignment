import json
from random import choice, choices, sample, randint, random, gauss
_roles = {"dev": 2, "art": 2, "gd": 2, "sound": 1, "pm": 1, "ux": 1}
_workloads = {"dev": (1, 2), "art": (1, 2), "gd": (1,), "sound": (.5, 1), "pm": (.5, 1), "ux": (.5, 1)}
_dummy_pitches = [
	"Minecraft but better", "Minecraft but worse", "Candy Clicker",
	"Covid: Isolation", "Doki doki Chess Club", "Dark Sels",
	"Bioshocolatine", "Basketball Physics", "Croissant Crush",
	"Pokimon Autobattler", "Sound Racer", "Final Emblem",
	"Dufos", "Muffin Party", "Lea Passion F1",
	"Straight Fighter", "SoloQ Simulator", "Abovetale",
	"Underwatch", "Tic-tac-toe Royale", "Stardew Mountains",
	"Gacha Impact", "Snakes 4: Mayhem", "Ori and the deaf Woodland"
]


def generate(size=1):
	# generate students with main roles and alternative roles
	with open("dummy_names.txt", "r") as fnames:
		names = fnames.read().splitlines()
	students = sample(names, size*30+randint(-3, 3))
	roles_w = list(_roles.values())
	roles_w = [w/sum(roles_w) for w in roles_w]
	roles_n = list(_roles.keys())
	# we add 1 role of each to make sure every roles are covered
	roles = roles_n+choices(roles_n, roles_w, k=len(students)-len(roles_n))
	rolesalt = choices(roles_n, [.4, .3, 0, .3, 0, 0], k=len(students))
	students_by_role = {role: [] for role in _roles}
	for student, role in zip(students, roles):
		students_by_role[role].append(student)
	# generate random pitches
	pitches = sample(_dummy_pitches, min(size*8+randint(0, 2), len(_dummy_pitches)))
	pitches_mean = [randint(5, 9) for _ in range(len(pitches))]
	pa_w = [.05, .1, .3, .05, .45, .05]
	authors = [
		choice(students_by_role[role])
		for role in choices(roles_n, pa_w, k=len(pitches))
	]
	workloads = [
		{
			role: choice(loads)
			for role, loads in _workloads.items()
		}
		for _ in pitches
	]
	with open("dummy_pitches.json", "w") as fpitches:
		json.dump({
			pitch: {"author": author, "workload": workload}
			for pitch, author, workload in zip(pitches, authors, workloads)
		}, fpitches, indent=4)
	# generate random wishes
	wishes = {}
	for student, role, rolealt in zip(students, roles, rolesalt):
		wishes[student] = []
		for pitch, author, mean in zip(pitches, authors, pitches_mean):
			if author == student:
				if random() < .8:
					wishes[student].append((pitch, "pm", 11))
				else:
					wishes[student].append((pitch, role, 11))
			else:
				rate = max(min(gauss(mean, 3), 10), 0)
				wishes[student].append((pitch, role, rate))
				ratealt = max(min(gauss(mean, 3), 10), 0)
				if ratealt > rate and random() < .5:
					wishes[student].append((pitch, rolealt, ratealt))
		wishes[student] = [
			(pitch, role)
			for pitch, role, _ in sorted(
				wishes[student], key=lambda prr: prr[2], reverse=True
			)
		]
	with open("dummy_wishes.json", "w") as fwishes:
		json.dump(wishes, fwishes, indent=4)


if __name__ == "__main__":
	generate(2)
