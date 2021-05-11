# PitchAssignment
Pitch assignment algorithm for game creation school

## Problem statement
`n` pitches with their associated workloads are proposed by students.  
After seeing the pitches, each student gives a ranking of `(pitch, role)` for every pitch.  

The goal of the algorithm is to assign students to pitches s.t. :
- the pitches with students are completable
- the motivation of the students is maximised

The algorithm should be flexible enough to consider solutions in which workload is divided
(2 programmers might take the work of 1) and pitches workload requirements are not perfectly met.  
The algorithm shall be parametrized with:
- `α` The weight given to bad ranks (students that work on a project they dislike)
- `β` The weight given to the respect of workload requirements

## Formalism

### Solution
A solution is a collection of `<student, [(pitch, role)]>` s.t. every student is present in the solution and students are always assigned to a `(pitch, role)` they did rank.

### Cost function
A cost function maps a solution to a real number (lower = better), 
taking into account the pitches requirements and the wishes of the students.

The cost function that we chose is:  
Given a solution `s`, `cost(s) = h(s) + p(s)`, with:
- `h(s) = Σ rank(s[i])^α` the sum of the ranks of the wishes fulfilled by `s`, with `α` controlling the weight given to bad ranks.
- `p(s)` the total deviation of the solution from the workload required by each pitch (`^β`), a greater cost will be attributed if there's less workers on a required task than if there's more.

### Algorithm
The goal is to minimize the cost function, with no assumptions on convexity.  
Given the huge number of possible solutions, a bruteforce to find the global minimum seems intractable.  
For now, we chose an evolutionnary technique that will start with a number of random solutions, keeping the bests and tweaking them at the next iteration.  
This will offer a trade-off between speed and the amount of local minima covered.
