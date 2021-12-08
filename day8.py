#!/usr/bin/env python3

from get_aoc import get_input_lines
from functools import reduce

UNIQUE_LENGTHS = {2, 3, 4, 7}

def normalize(string):
    return [set(term) for term in string.split()]

class Display:
    def __init__(self, notes):
        patterns, output = notes.split(' | ')
        self.patterns = normalize(patterns)
        self.output = normalize(output)

        one   = self.find(2)
        seven = self.find(3)
        four  = self.find(4)
        eight = self.find(7)

        three = self.find(5, seven)
        zero  = self.find(6, seven, eight - three)
        nine  = self.find(6, three)
        six   = self.find(6)

        five  = self.find(5, four - one)
        two   = self.find(5)

        self.digits = [zero, one, two, three, four, five, six, seven, eight, nine]

    def find(self, length, *subsets):
        match = next(p for p in self.patterns if len(p) == length and
                                                 all(s.issubset(p) for s in subsets))
        self.patterns.remove(match)
        return match

    def part_one(self):
        return sum(len(digit) in UNIQUE_LENGTHS for digit in self.output)

    def part_two(self):
        return reduce(lambda val, digit: val * 10 + self.digits.index(digit), self.output, 0)

displays = [Display(line) for line in get_input_lines(8)]

print("Part 1:")
print(sum(display.part_one() for display in displays))

print("Part 2:")
print(sum(display.part_two() for display in displays))
