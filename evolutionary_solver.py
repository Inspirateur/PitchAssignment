from bisect import bisect_right
from collections import defaultdict
from copy import copy
import math
from functools import lru_cache
try:
    from Pyewacket import choices, random, sample
except ImportError:
    print(
        "INFO: Try to install Pyewacket if you can, it can speed up the process. " +
        "https://pypi.org/project/Pyewacket/ \n"
    )
    from random import choices, random, sample
import itertools
from time import time
from cost import Cost


@lru_cache()
def exp_cum(n):
    return list(itertools.accumulate(math.exp(1-(i+1/n)) for i in range(n)))


def random_wish(rankings):
    """
    Select a wish randomly with exponential decay
    :param rankings: ordered [(pitch, role)]
    :return: i the index of the chosen wish in the rankings
    """
    cum_weights = exp_cum(len(rankings))
    total = cum_weights[-1]
    hi = len(cum_weights) - 1
    return bisect_right(cum_weights, random()*total, 0, hi)


def random_solutions(wishes, n):
    """
    :param wishes: <student, [(pitch, role)]>
    :param n: int
    :return: [student, wish index]
    """
    return [
        {
            (student, random_wish(wishes[student]))
            for student in wishes
        }
        for _ in range(n)
    ]


def student_tasks(solution, student1):
    studenttasks = 0
    for student2, _ in solution:
        if student2 == student1:
            studenttasks += 1
    return studenttasks


def random_changes(wishes, solution, k):
    """
    Apply k random changes to a solution
    :param wishes: <student, [(pitch, role)]>
    :param solution: {student, wish index}
    :param k: int
    :return: the new solution
    """
    tasks = sample(solution, k=k)
    for student, i in tasks:
        newtask = (student, random_wish(wishes[student]))
        if random() < .8:
            # just change a task
            solution.remove((student, i))
            solution.add(newtask)
        else:
            # add/remove a task
            if student_tasks(solution, student) == 1:
                solution.add(newtask)
            else:
                solution.remove((student, i))


def solve(pitches, wishes, relations=None, n=200, patience=200, diversity=.9):
    """
    Attempt to minimise the cost function with a naive evolutionnary solver
    :param pitches: <pitch, <role, load>>
    :param wishes: <student, [(pitch, role)]>
    :param relations: <student, <student, cost>>
    :param n: number of competing solutions
    :param patience: number of iteration without improvement before stopping
    :param diversity: proportion of kept solutions for the next iteration
    :return: [(student, wish index)]
    """
    assert n > 1 and patience > 0
    cost = Cost(pitches, wishes, relations)
    # precomputations to pick best solutions to clone and modify
    keep = int(n*diversity)
    discard = list(range(keep-1, n))
    # the starting solutions {student, wish index}
    solutions = random_solutions(wishes, n)
    p = patience
    # for printing in the console with padded 0
    zfill_p = len(str(patience))-1
    best_cost = float("+inf")
    print("Cost so far:")
    start = time()
    count = 0
    while p > 0:
        count += 1
        # compute the cost of the solutions
        costs = [cost(s) for s in solutions]
        # sort the solutions by cost
        costs, solutions = zip(
            *sorted(zip(costs, solutions), key=lambda cs: cs[0]))
        solutions = list(solutions)
        # update the patience
        if best_cost == costs[0]:
            p -= 1
        else:
            p = patience
            best_cost = costs[0]
        print(
            f"{best_cost:.2f}  (patience = {str(int(p/10)).zfill(zfill_p)}) ", end="\r")
        # replace the worse solutions by modified clones of the best solutions
        for i in discard:
            solutions[i] = copy(solutions[i % keep])
            random_changes(wishes, solutions[i], 2)
    print()
    delta = time()-start
    print(f"in {delta:,.1f} sec - {1000*delta/count:.0f}ms/it")
    # [(student, wish index)]
    return solutions[0]
