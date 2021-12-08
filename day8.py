#!/usr/bin/env python3

from get_aoc import get_input_lines
from functools import reduce

UNIQUE_LENGTHS = {2, 3, 4, 7}

def normalize(strings):
    return [set(string) for string in strings]

class Display:
    def __init__(self, notes):
        patterns, output = notes.split(' | ')
        self.patterns = normalize(patterns.split())
        self.output = normalize(output.split())

        one   = self.find(lambda p: len(p) == 2)
        seven = self.find(lambda p: len(p) == 3)
        four  = self.find(lambda p: len(p) == 4)
        eight = self.find(lambda p: len(p) == 7)

        three = self.find(lambda p: len(p) == 5 and seven.issubset(p))
        zero  = self.find(lambda p: p != seven and seven.issubset(p) and not three.issubset(p))
        nine  = self.find(lambda p: len(p) == 6 and three.issubset(p))
        six   = self.find(lambda p: len(p) == 6 and p != zero and p != nine)

        five  = self.find(lambda p: len(p) == 5 and p.issubset(six))
        two   = self.find(lambda p: len(p) == 5 and p != three and p != five)

        self.digits = [zero, one, two, three, four, five, six, seven, eight, nine]


    def find(self, predicate):
        return next(pattern for pattern in self.patterns if predicate(pattern))

    def part_one(self):
        return sum(len(digit) in UNIQUE_LENGTHS for digit in self.output)

    def part_two(self):
        return reduce(lambda val, digit: val * 10 + self.digits.index(digit), self.output, 0)

displays = [Display(line) for line in get_input_lines(8)]

print("Part 1:")
print(sum(display.part_one() for display in displays))

print("Part 2:")
print(sum(display.part_two() for display in displays))
