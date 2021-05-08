# PitchAssignment
Pitch assignment algorithm for game creation school

## Problem statement
`n` pitches with their associated workloads are proposed by students.  
Each student gives a ranking of `(pitch, role)` for every pitch.  
The goal of the algorithm is to assign students to pitches s.t. :
- the pitches with students are completable
- the motivation of the students is maximised

The algorithm should be flexible enough to consider solutions in which workload is divided
(2 programmers might take the work of 1) and pitches workload requirements are not perfectly met.  
The algorithm shall be parametrized with:
- The weight given to bad ranks (students that work on a project they dislike)
- The weight given to the respect of workload requirements

## Formalism

### Solution
A solution is a collection of `(student, pitch, role)` s.t. every student is present in the solution.

### Cost function
A cost function has to score a solution (with a real number), 
taking into account the pitches requirements and the wishes of the students.

The cost function that we chose is: **TO BE DEFINED**

### Algorithm
The goal is to minimize the cost function, with no assumptions on convexity.  
Given the huge number of possible solutions, a bruteforce to find the global minimum seems intractable.  
For now, we chose an evolutionnary technique that will start with a number of random solutions, keeping the bests and tweaking them at the next iteration.  
This will offer a trade-off between speed and the amount of local minima covered.
