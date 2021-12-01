#!/usr/bin/env python3

from get_aoc import get_input_integers

depths = get_input_integers(1)

increments = 0
for i in range(len(depths) - 1):
    if depths[i] < depths[i+1]:
        increments += 1

print("Part 1:")
print(increments)

increments = 0
for i in range(len(depths) - 3):
    if sum(depths[i:i+3]) < sum(depths[i+1:i+4]):
        increments += 1

print("Part 2:")
print(increments)
