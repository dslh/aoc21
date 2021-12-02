#!/usr/bin/env python3

from get_aoc import get_input_lines

lines = [line.split(' ') for line in get_input_lines(2)]
instructions = [(direction, int(distance)) for (direction, distance) in lines]

def total_direction(instructions, direction):
    return sum(distance for (direct, distance) in instructions if direction == direct)

forward = total_direction(instructions, 'forward')
depth = total_direction(instructions, 'down') - total_direction(instructions, 'up')

print("Part 1:")
print(forward * depth)

depth = 0
dir = 0

for instruction, amount in instructions:
    if instruction == 'forward':
        depth += amount * dir
    elif instruction == 'down':
        dir += amount
    elif instruction == 'up':
        dir -= amount

print("Part 2:")
print(forward * depth)
