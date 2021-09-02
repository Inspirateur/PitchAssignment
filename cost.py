from collections import defaultdict
MULTITASK_PENALTY = .2


def wishes_cost(wishes, solution):
	"""
	cost of the wishes not being respected
	:param wishes: <student, [(pitch, role)]>
	:param solution: [student, wish index]
	:return: float
	"""
	return sum(
		((i+1)/len(wishes[student]))**2
		for student, i in solution
	)


def workload_diff(target, proposed):
	"""
	Helper for pitches_cost
	:param target: <role, load>
	:param proposed: <role, load>
	:return: float
	"""
	total = 0
	for role in target:
		# flat penalty of -1 if no students are on a target role
		diff = target[role]-(proposed[role] if role in proposed else -1)
		# the squared diff is added to the cost (so that greater discrepencies cost more)
		total += diff**2
	return total


def pitches_cost(pitches, wishes, solution):
	"""
	cost of the pitches workload not being respected
	:param pitches: <pitch, <role, load>>
	:param wishes: <student, [(pitch, role)]>
	:param solution: [student, wish index]
	:return: float
	"""
	tasks_per_students = defaultdict(int)
	for student, _ in solution:
		tasks_per_students[student] += 1
	workloads = defaultdict(lambda: defaultdict(float))
	for student, i in solution:
		pitch, role = wishes[student][i]
		workloads[pitch][role] += 1/tasks_per_students[student]
	# a penalty per additionnal task per student is added to avoid students multitasking too much
	return (
		# cost of workload diff between requirements and solution
		sum(
			workload_diff(pitches[pitch]["workload"], workloads[pitch])
			for pitch in pitches
			if pitch in workloads
		)
		# cost of multitasking
		+ sum(tasks-1 for tasks in tasks_per_students.values())*MULTITASK_PENALTY
		# cost of author not having their roles
		+ 2*author_constraint(pitches, wishes, solution)
	)


def author_tasks(pitches, wishes):
	tasks = {}
	for pitch in pitches:
		author = pitches[pitch]["author"]
		for wpitch, role in wishes[author]:
			if wpitch == pitch:
				tasks[(wpitch, role)] = author
	return tasks


def author_constraint(pitches, wishes, solution):
	"""
	cost of the authors not getting their roles on their pitch
	:param pitches: <pitch, <role, load>>
	:param wishes: <student, [(pitch, role)]>
	:param solution: [student, wish index]
	:return: float
	"""
	# <(pitch, role), author>
	tasks = author_tasks(pitches, wishes)
	tasks_solution = {task: None for task in tasks}
	for student, i in solution:
		pitch, role = wishes[student][i]
		if (pitch, role) in tasks:
			if student == tasks[(pitch, role)] or tasks_solution[(pitch, role)] is None:
				tasks_solution[(pitch, role)] = student
	author_cost = 0
	for task, student in tasks_solution.items():
		if student is not None and student != tasks[task]:
			author_cost += 1
	return author_cost


def cost(pitches, wishes, solution, alpha=1, beta=2):
	return (
		alpha*wishes_cost(wishes, solution) +
		beta*pitches_cost(pitches, wishes, solution)
	)/(alpha+beta)
