from itertools import combinations
from cost import cost
import operator as op
from functools import reduce


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom


def restrict_pitches(pitches: dict, select_pitches: set):
    return {pitch: workload for pitch, workload in pitches.items() if pitch in select_pitches}


def restrict_wishes(wishes, select_pitches: set):
    return {
        student: [(pitch, role)
                  for pitch, role in ranking if pitch in select_pitches]
        for student, ranking in wishes.items()
    }


def fixed_pitch_solve(solver, pitches, wishes, relations, n):
    """
    Call the solver for every possible combinations of n pitches, thus forcing the amount of pitches to n.
    Returns the best solution of all calls
    :param pitches: <pitch, <role, load>>
    :param wishes: <student, [(pitch, role)]>
    :param relations: <student, <student, cost>>
    :param n: final number of pitches in solution
    :return: [(student, wish index)]
    """
    pitch_list = list(pitches.keys())
    assert len(pitch_list) >= n
    print(
        f"Bruteforcing all combinations of {n} in {len(pitch_list)} pitches"
    )
    total = ncr(len(pitch_list), n)
    best_solution = None
    best_cost = float("+inf")
    for i, select_pitches in enumerate(combinations(pitch_list, n)):
        print(f"{i}/{total}  best cost = {best_cost} ", end="\r")
        select_pitches = set(select_pitches)
        _pitches = restrict_pitches(pitches, select_pitches)
        _wishes = restrict_wishes(wishes, select_pitches)
        solution = solver(_pitches, _wishes, relations)
        new_cost = cost(_pitches, _wishes, solution, relations)
        if new_cost < best_cost:
            best_cost = new_cost
            best_solution = solution
    return best_solution
