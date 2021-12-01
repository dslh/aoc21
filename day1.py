#!/usr/bin/env python3

from get_aoc import get_input_integers

depths = get_input_integers(1)

print("Part 1:")
print(sum(a < b for (a, b) in zip(depths[:-1], depths[1:])))

print("Part 2:")
windows = list(zip(depths[:-2], depths[1:-1], depths[2:]))
print(sum(sum(a) < sum(b) for (a, b) in zip(windows[:-1], windows[1:])))
