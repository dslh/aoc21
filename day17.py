#!/usr/bin/env python3

import re
from math import ceil

def parse(input):
    x1,x2, y1,y2 = [int(n) for n in re.findall(r'-?\d+', input)]
    return ((x1,x2), (y1,y2))

def limits(area):
    x, y = area

    min_x = ceil(((x[0] * 8 + 1) ** 0.5 - 1) / 2)
    max_x = ceil(x[1] / 2)

    min_y = y[0] // 2 + 1
    max_y = abs(y[0] + 1)

    return ((min_x, max_x), (min_y, max_y))

def max_height(area):
    _, (_,y) = limits(area)
    return (y**2 + y) // 2

def valid_trajectory(area, vx, vy):
    (min_x, max_x), (min_y, max_y) = area
    x = vx
    y = vy

    while x <= max_x and y >= min_y:
        if x >= min_x and y <= max_y:
            return True

        if vx > 0:
            vx -= 1
        vy -= 1

        x += vx
        y += vy

    return False

def inclusive(limits):
    a, b = limits
    return range(a, b + 1)

def all_trajectories(area):
    x_lim, y_lim = limits(area)

    trajectories = {(x,y) for x in inclusive(x_lim) for y in inclusive(y_lim) if valid_trajectory(area, x, y)}

    return trajectories | {(x,y) for x in inclusive(area[0]) for y in inclusive(area[1])}

if __name__ == '__main__':
    from get_aoc import get_input

    area = parse(get_input(17))

    print("Part 1:")
    print(max_height(area))

    print("Part 2:")
    print(len(all_trajectories(area)))
