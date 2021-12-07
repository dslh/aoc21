#!/usr/bin/env python3

from get_aoc import get_input_integers

crabs = get_input_integers(7, ',')
crab_range = range(min(crabs), max(crabs))

def fuel_cost(crabs, pos):
    return sum(abs(crab - pos) for crab in crabs)

best_pos = min(crab_range, key=lambda pos : fuel_cost(crabs, pos))

print("Part 1:")
print(fuel_cost(crabs, best_pos))

def geometric_cost(crab, pos):
    dist = abs(crab - pos)
    return dist * (dist + 1) // 2

def geometric_fuel_cost(crabs, pos):
    return sum(geometric_cost(crab, pos) for crab in crabs)

best_pos = min(crab_range, key=lambda pos: geometric_fuel_cost(crabs, pos))

print("Part 2:")
print(geometric_fuel_cost(crabs, best_pos))
