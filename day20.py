#!/usr/bin/env python3

from get_aoc import get_input_chunks

rules, image = get_input_chunks(20)
rules = [rule == '#' for rule in rules]
image = image.split('\n')

positives = {(i,j) for i in range(len(image))
                      for j in range(len(image[0]))
                      if image[i][j] == '#'}

# Flipped from the problem description, because rather than checking
# a position's neighbours to determine its new state, we apply a position
# to its neighbours to determine their new state.
RULE_MASK = [
    [0b000000001, 0b000000010, 0b000000100],
    [0b000001000, 0b000010000, 0b000100000],
    [0b001000000, 0b010000000, 0b100000000]
]
def rule_mask(d_i, d_j):
    return RULE_MASK[d_i + 1][d_j + 1]

NEIGHBOURS = [(i,j) for i in range(-1,2) for j in range(-1,2)]

# Since after the first step we end up with an infinite field of light pixels,
# we need to return a set including only dark pixels.
def negative_enhance(positives, rules):
    negatives = dict()
    for i, j in positives:
        for d_i, d_j in NEIGHBOURS:
            pos = (i + d_i, j + d_j)
            if pos not in negatives:
                negatives[pos] = 0

            negatives[pos] |= rule_mask(d_i, d_j)

    return {pos for pos, rule in negatives.items() if not rules[rule]}

# ...then on the subsequent step the infinite field is going to go dark again,
# so we need to return a set of light pixels.
def positive_enhance(negatives, rules):
    positives = dict()
    for i, j in negatives:
        for d_i, d_j in NEIGHBOURS:
            pos = (i + d_i, j + d_j)
            if pos not in positives:
                positives[pos] = 0b111111111

            positives[pos] &= ~rule_mask(d_i, d_j)

    return {pos for pos, rule in positives.items() if rules[rule]}

negatives = negative_enhance(positives, rules)
print("Part 1:")
print(len(positive_enhance(negatives, rules)))

for _ in range(25):
    negatives = negative_enhance(positives, rules)
    positives = positive_enhance(negatives, rules)

print("Part 2:")
print(len(positives))

