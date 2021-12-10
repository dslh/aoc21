#!/usr/bin/env python3

from get_aoc import get_input_lines
from functools import reduce
from statistics import median

PARENS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

ERROR_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

def error_score(line):
    parens = []
    for c in line:
        if c in PARENS:
            parens.append(c)
        else:
            if not parens or c != PARENS[parens[-1]]:
                return ERROR_SCORES[c]
            else:
                parens.pop()

    return 0

lines = get_input_lines(10)

print('Part 1:')
print(sum(error_score(line) for line in lines))
