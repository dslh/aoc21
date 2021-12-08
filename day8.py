#!/usr/bin/env python3

from get_aoc import get_input_lines

UNIQUE_LENGTHS = {2, 3, 4, 7}

class Display:
    def __init__(self, notes):
        patterns, output = notes.split(' | ')
        self.patterns = patterns.split()
        self.output = output.split()

    def part_one(self):
        return sum(len(digit) in UNIQUE_LENGTHS for digit in self.output)

displays = [Display(line) for line in get_input_lines(8)]

print("Part 1:")
print(sum(display.part_one() for display in displays))
