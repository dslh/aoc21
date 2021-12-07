#!/usr/bin/env python3

from get_aoc import get_input_integers

crabs = get_input_integers(7, ',')

def fuel_cost(crabs, pos):
    return sum(abs(crab - pos) for crab in crabs)

best_pos = min(range(min(crabs), max(crabs)), key=lambda pos : fuel_cost(crabs, pos))

print("Part 1:")
print(fuel_cost(crabs, best_pos))
