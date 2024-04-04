# Overview
We seek to implement an exact quantum algorithm for the Traveling Salesperson Problem using Quantum Phase Estimation and Grover's Search Algorithm. 

# The Traevling Salesperson Problem
Imagine our salesperson resides in a region with $N$ cities. Each city is connected to at least one other city. The salesperson, starting from city $C_0$, wants to take a path whereby:
* He visits every city exactly once
* He returns back to the city $C_0$ that he started at
* The path he takes is the shortest path possible.
A naive, brute force exact algorithm consists of checking every possible path. This corresponds to some permutation of the $N$ cities, of which there are $N!$ permutations.

