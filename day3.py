#!/usr/bin/env python3

from get_aoc import get_input_lines

lines = get_input_lines(3)
WIDTH = range(len(lines[0]))
numbers = [int(line, 2) for line in lines]

counts = {i:0 for i in WIDTH}
for number in numbers:
    for i in WIDTH:
        if (1 << i) & number:
            counts[i] += 1

threshold = len(lines) / 2

gamma = 0
epsilon = 0

for i in WIDTH:
    if counts[i] > threshold:
        gamma |= 1 << i
    else:
        epsilon |= 1 << i

print("Part 1:")
print(gamma * epsilon)
