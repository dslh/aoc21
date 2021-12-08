#!/usr/bin/env python3

from get_aoc import get_input_lines
from functools import reduce

UNIQUE_LENGTHS = {2, 3, 4, 7}

# Since the same digit may appear with its segments in different orders,
# and since we want to deduce digits based on a subset of the lit segments,
# we convert them into sets.
def normalize(string):
    return [set(term) for term in string.split()]

class Display:
    def __init__(self, notes):
        digits, output = notes.split(' | ')

        # Convert all words in the input into sets
        self.digits = normalize(digits)
        self.output = normalize(output)

        # Figuring out which digit is which
        # Starting with digits of unique length
        one   = self.find(2)
        seven = self.find(3)
        four  = self.find(4)
        eight = self.find(7)

        # Digits with 5 lit segments
        # Three is the only 5-segment that has contains all the segments of 7
        three = self.find(5, seven)
        # Find five based on the elbow shape that is in four but not in 1
        five  = self.find(5, four - one)
        # Two is then the only remaining 5-segment digit
        two   = self.find(5)

        # And so on for 6-segment digits
        # Eight minus three gives us the two left segments, plus seven is almost
        # the same shape as zero, just missing the bottom segment
        zero  = self.find(6, seven | (eight - three))
        # Nine is three but with one extra segment lit up
        nine  = self.find(6, three)
        # Six is then the only remaining digit
        six   = self.find(6)

        # Put the digits back into the array so that their index matches their value
        self.digits = [zero, one, two, three, four, five, six, seven, eight, nine]

    # Find a digit in the list that has:
    # - A given number of segments lit up when displayed
    # - At least the given subset of segments lit up
    #
    # Removes digits from the list as they are found,
    # to make subsequent digits easier to find.
    def find(self, length, subset=set()):
        match = next(p for p in self.digits if len(p) == length and subset.issubset(p))
        self.digits.remove(match)
        return match

    # Part one: Count the digits appearing on the readout that have
    # a unique number of lit segments. i.e. 1, 3, 4 and 7
    def part_one(self):
        return sum(len(digit) in UNIQUE_LENGTHS for digit in self.output)

    # Part two: Work out what value the readout is actually displaying
    def part_two(self):
        # Work out the value of a digit based on its index in the sorted list.
        # Add them up from left to right, but before adding each new digit, multiply the
        # accumulated value by ten. That's how base 10 numbers work.
        return reduce(lambda val, digit: val * 10 + self.digits.index(digit), self.output, 0)

displays = [Display(line) for line in get_input_lines(8)]

print("Part 1:")
print(sum(display.part_one() for display in displays))

print("Part 2:")
print(sum(display.part_two() for display in displays))
