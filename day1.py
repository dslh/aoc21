#!/usr/bin/env python3

from collections import deque

def windowed(iterable, size=2):
    q = deque([], size)
    for item in iterable:
        q.append(item)
        if len(q) == size:
            yield list(q)

def count_increases(lst, window=1):
    return sum(sum(a) < sum(b) for (a, b) in windowed(windowed(lst, window), 2))

if __name__ == '__main__':
    from get_aoc import get_input_integers

    depths = get_input_integers(1)

    print("Part 1:")
    print(count_increases(depths))

    print("Part 2:")
    print(count_increases(depths, 3))
