#!/usr/bin/env python3

import re
from functools import reduce
from itertools import chain

# For parsing things like x=10..12,y=10..12,z=10..12
def parse_cube(specifier):
    return Cube(*[int(i) for i in re.findall(r'-?\d+', specifier)])

class Cube:
    def __init__(self, x_a, x_b, y_a, y_b, z_a, z_b):
        self.x_a = x_a
        self.x_b = x_b
        self.y_a = y_a
        self.y_b = y_b
        self.z_a = z_a
        self.z_b = z_b

    def volume(self):
        return (
            (self.x_b - self.x_a + 1) *
            (self.y_b - self.y_a + 1) *
            (self.z_b - self.z_a + 1)
        )

    def __and__(self, other):
        return (
            self.x_a <= other.x_b and
            self.x_b >= other.x_a and
            self.y_a <= other.y_b and
            self.y_b >= other.y_a and
            self.z_a <= other.z_b and
            self.z_b >= other.z_a
        )

    def __sub__(self, other):
        if not (self & other):
            return [self]

        out = []

        if other.z_a > self.z_a:
            out.append(Cube(
                self.x_a, self.x_b,
                self.y_a, self.y_b,
                self.z_a, other.z_a - 1
            ))

        if other.z_b < self.z_b:
            out.append(Cube(
                self.x_a, self.x_b,
                self.y_a, self.y_b,
                other.z_b + 1, self.z_b
            ))

        z_a = max(self.z_a, other.z_a)
        z_b = min(self.z_b, other.z_b)

        if other.y_a > self.y_a:
            out.append(Cube(
                self.x_a, self.x_b,
                self.y_a, other.y_a - 1,
                z_a, z_b
            ))

        if other.y_b < self.y_b:
            out.append(Cube(
                self.x_a, self.x_b,
                other.y_b + 1, self.y_b,
                z_a, z_b
            ))

        y_a = max(self.y_a, other.y_a)
        y_b = min(self.y_b, other.y_b)

        if other.x_a > self.x_a:
            out.append(Cube(
                self.x_a, other.x_a - 1,
                y_a, y_b, z_a, z_b
            ))

        if other.x_b < self.x_b:
            out.append(Cube(
                other.x_b + 1, self.x_b,
                y_a, y_b, z_a, z_b
            ))

        return out

def subtract_from_all(cubes, cube):
    return list(chain.from_iterable(c - cube for c in cubes))

def execute(field, instruction):
    cmd, specifier = instruction.split(' ', 1)
    cube = parse_cube(specifier)

    if cmd == 'on':
        return field + reduce(subtract_from_all, field, [cube])
    else:
        return subtract_from_all(field, cube)

def execute_all(instructions):
    return reduce(execute, instructions, [])

if __name__ == '__main__':
    from get_aoc import get_input_lines

    instructions = get_input_lines(22)

    init_area = Cube(*([-50, 50] * 3))
    init_instructions = [i for i in instructions if parse_cube(i.split(' ')[1]) & init_area]

    print('Part 1:')
    print(sum(cube.volume() for cube in execute_all(init_instructions)))

    print('Part 2:')
    print(sum(cube.volume() for cube in execute_all(instructions)))
