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

## Formalism

### Solution
A solution is a collection of `<pitch, <role, [students]>` s.t. every student is present in the solution and students are always assigned to a `(pitch, role)` they did rank.

### Cost function
A cost function maps a solution to a real number (lower = better), 
taking into account the pitches requirements and the wishes of the students.

The cost function that we chose is:  
Given a solution `s`, `cost(s) = α*w(s) + (1-α)*r(s)`, with:
- `w(s)` the cost of the wishes fulfilled by `s`, if the solution grants top wishes of the students the score will be low.
- `r(s)` the cost of the requirements fulfilled by `s`. Which includes:
  - deviation of the solution from the workload required by each pitch  
    (for example the solution will be penalized if there's not enough programmer on one pitch)
  - the cost of an author not having their role on their pitch.
  - the cost of students multi-tasking, which needs to be avoided if possible

The cost function is parametrized by α in [0, 1], which we call "flexibility",  
a greater α will give less importance to the requirements.

### Algorithm
The goal is to minimize the cost function, with no assumptions on convexity.  
Given the huge number of possible solutions, a bruteforce to find the global minimum seems intractable.  
For now, we chose an evolutionnary technique that will start with a number of random solutions, keeping the bests and tweaking them at the next iteration.  
This will offer a trade-off between speed and the amount of local minima covered.
