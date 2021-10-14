import json
from evolutionary_solver import solve
from bruteforce_pitches import fixed_pitch_solve
from cost import cost
from dummy_data import generate
from collections import defaultdict
import cProfile


def pretty_wishes(wishes):
    res = {}
    for student, ranking in wishes.items():
        res[student] = {
            task: f"{i+1}/{len(ranking)}"
            for i, task in enumerate(ranking)
        }
    return res


def print_solution(pitches, wishes, solution):
    """
    :param pitches: <pitch, <role, load>>
    :param wishes: <student, [(pitch, role)]>
    :param solution: <pitch, <role, [student]>>
    """
    wishes = pretty_wishes(wishes)
    for pitch in solution:
        print(f"{pitch} ({pitches[pitch]['author']})")
        for role, load in pitches[pitch]['workload'].items():
            students = [
                f"{student} {wishes[student][(pitch, role)]}" for student in solution[pitch][role]]
            print(f"\t{role} ({load}):", ", ".join(students))
        print()


def load_solution(file, wishes):
    with open(file, "r") as fsolution:
        _solution = json.load(fsolution)
    solution = []
    for pitch, workers in _solution.items():
        for role, students in workers.items():
            for student in students:
                i = wishes[student].index((pitch, role))
                solution.append((student, i))
    return solution


def format_solution(solution, wishes):
    """
    :param solution: [(student, wish index)]
    :return: <pitch, <role, [students]>>
    """
    res = defaultdict(lambda: defaultdict(list))
    for student, i in solution:
        pitch, role = wishes[student][i]
        res[pitch][role].append(student)
    return res


def _test_solve():
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
    with open("dummy_relations.json", "r") as frels:
        relations = json.load(frels)
    solution = format_solution(
        solve(pitches, wishes, relations),
        wishes
    )
    print_solution(pitches, wishes, solution)
    with open("solution.json", "w") as fsolution:
        json.dump(solution, fsolution, indent=2)


def test_solve():
    try:
        _test_solve()
    except OSError:
        print("No data provided, the program will be tested on fake generated data.\n")
        generate(1)
        _test_solve()


def test_load(file="solution.json"):
    with open("dummy_pitches.json", "r") as fpitches:
        # pitches[pitch]["workload"]: <role, load>
        # pitches[pitch]["author"]: a student
        pitches = json.load(fpitches)
    with open("dummy_wishes.json", "r") as fwishes:
        wishes = json.load(fwishes)
    # reconvert the tuples that got converted to list with json
    for student, ranking in wishes.items():
        wishes[student] = [(pitch, role) for pitch, role in ranking]
    with open("dummy_relations.json", "r") as frels:
        relations = json.load(frels)
    solution = load_solution(file, wishes)
    c = cost(pitches, wishes, solution, relations)
    print(f"{file} cost: {c:.2f}")


if __name__ == "__main__":
    test_solve()
