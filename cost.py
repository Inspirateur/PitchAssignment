from collections import defaultdict
from itertools import product
MULTITASK_PENALTY = 1
AUTHOR_PENALTY = 2
RELATION_COST = .05
DEFAULT_FLEXIBILITY = .1
OVERREQ_PENALTY = 0.5


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
        diff = target[role] - (proposed[role] if role in proposed else -1)
        # a negative diff means too much student were assigned on the role
        if diff < 0:
            # the penalty for going over requirements can be softened
            diff *= OVERREQ_PENALTY
        # the squared diff is added to the cost (so that greater discrepencies cost more)
        total += diff ** 2
    return total


def author_tasks(pitches, wishes):
    tasks = {}
    for pitch in pitches:
        author = pitches[pitch]["author"]
        for wpitch, role in wishes[author]:
            if wpitch == pitch:
                tasks[(wpitch, role)] = author
    return tasks


class Cost:
    def __init__(self, pitches, wishes, relations=None, flexibility=DEFAULT_FLEXIBILITY):
        """
        :param pitches:  <pitch, <role, load>>
        :param wishes: <student, [(pitch, role)]>
        :param relations: <student, <student, cost>>
        :param flexibility: float in [0, 1]
        """
        self.pitches = pitches
        self.wishes = wishes
        self.relations = relations if relations else {}
        self.flexibility = flexibility
        self.author_tasks = author_tasks(pitches, wishes)

    def __call__(self, solution):
        return (
            (1 - self.flexibility) * self.pitches_cost(solution) +
            self.flexibility * (self.wishes_cost(solution) +
                                RELATION_COST*self.relations_cost(solution))
        )

    def author_constraint(self, solution):
        """
        cost of the authors not getting their roles on their pitch
        :param solution: [student, wish index]
        :return: float
        """
        # <(pitch, role), author>
        tasks_solution = {task: None for task in self.author_tasks}
        for student, i in solution:
            pitch, role = self.wishes[student][i]
            if (pitch, role) in self.author_tasks:
                if student == self.author_tasks[(pitch, role)] or tasks_solution[(pitch, role)] is None:
                    tasks_solution[(pitch, role)] = student
        author_cost = 0
        for task, student in tasks_solution.items():
            if student != self.author_tasks[task]:
                author_cost += 1
        return author_cost

    def pitches_cost(self, solution):
        """
        cost of the pitches workload not being respected
        :param solution: [student, wish index]
        :return: float
        """
        tasks_per_students = defaultdict(int)
        for student, _ in solution:
            tasks_per_students[student] += 1
        workloads = defaultdict(lambda: defaultdict(float))
        for student, i in solution:
            pitch, role = self.wishes[student][i]
            workloads[pitch][role] += 1/tasks_per_students[student]
        # a penalty per additionnal task per student is added to avoid students multitasking too much
        return (
            # cost of workload diff between requirements and solution
            sum(
                workload_diff(self.pitches[pitch]
                              ["workload"], workloads[pitch])
                for pitch in self.pitches
                if pitch in workloads
            )
            # cost of multitasking
            + MULTITASK_PENALTY * \
            sum(tasks-1 for tasks in tasks_per_students.values())
            # cost of author not having their roles
            + AUTHOR_PENALTY*self.author_constraint(solution)
        )

    def wishes_cost(self, solution):
        """
        cost of the wishes not being respected
        :param solution: [student, wish index]
        :return: float
        """
        return sum(
            ((i+1)/len(self.wishes[student]))**2
            for student, i in solution
        )

    def relations_cost(self, solution):
        """
        cost of the relations between students
        :param solution: [student, wish index]
        :return: float
        """
        groups = defaultdict(list)
        for student, i in solution:
            pitch, role = self.wishes[student][i]
            groups[pitch].append(student)
        total = 0
        for group in groups.values():
            for student, other in product(filter(self.relations.__contains__, group), group):
                if student != other:
                    if other not in self.relations[student]:
                        total += .5
                    elif self.relations[student][other] == -1:
                        total += 1
        return total


def cost(pitches, wishes, solution, relations=None, flexibility=DEFAULT_FLEXIBILITY):
    return Cost(pitches, wishes, relations, flexibility)(solution)
