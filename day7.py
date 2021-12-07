#!/usr/bin/env python3

from get_aoc import get_input_integers
import statistics, math

crabs = get_input_integers(7, ',')

best_pos = int(statistics.median(crabs))

print("Part 1:")
print(sum(abs(crab - best_pos) for crab in crabs))

def geometric_cost(crab, pos):
    dist = abs(crab - pos)
    return dist * (dist + 1) // 2

def geometric_fuel_cost(crabs, pos):
    return sum(geometric_cost(crab, pos) for crab in crabs)

best_pos = statistics.mean(crabs)
cost = min(geometric_fuel_cost(crabs, pos) for pos in [math.floor(best_pos), math.ceil(best_pos)])

print("Part 2:")
print(cost)
