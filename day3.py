#!/usr/bin/env python3

from get_aoc import get_input_lines

lines = get_input_lines(3)
WIDTH = range(len(lines[0]))
numbers = [int(line, 2) for line in lines]

def count_position(numbers, position):
    return sum((number & (1 << position)) != 0 for number in numbers)

counts = [count_position(numbers, i) for i in WIDTH]

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

def find_oxygen_rating(numbers):
    for i in reversed(WIDTH):
        count = count_position(numbers, i)
        threshold = len(numbers) / 2

        if count >= threshold:
            numbers = [n for n in numbers if n & (1 << i)]
        else:
            numbers = [n for n in numbers if ~n & (1 << i)]

        if len(numbers) == 1:
            return numbers[0]

oxygen_rating = find_oxygen_rating(numbers)

def find_scrubber_rating(numbers):
    for i in reversed(WIDTH):
        count = count_position(numbers, i)
        threshold = len(numbers) / 2

        if count >= threshold:
            numbers = [n for n in numbers if ~n & (1 << i)]
        else:
            numbers = [n for n in numbers if n & (1 << i)]

        if len(numbers) == 1:
            return numbers[0]

scrubber_rating = find_scrubber_rating(numbers)

print("Part 2:")
print(oxygen_rating * scrubber_rating)
