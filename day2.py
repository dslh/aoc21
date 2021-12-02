#!/usr/bin/env python3

from get_aoc import get_input_lines

lines = [line.split(' ') for line in get_input_lines(2)]
instructions = [(direction, int(distance)) for (direction, distance) in lines]

def total_direction(instructions, direction):
    return sum(distance for (direct, distance) in instructions if direction == direct)

forward = total_direction(instructions, 'forward')
down = total_direction(instructions, 'down') - total_direction(instructions, 'up')

print("Part 1:")
print(forward * down)
