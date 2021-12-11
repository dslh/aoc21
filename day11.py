#!/usr/bin/env python3

from get_aoc import get_input_lines

import os
from time import sleep
from colorama import init, Fore, Back, Style
init()

COLOURS = [
    Fore.CYAN  + Back.CYAN  + Style.BRIGHT,
    Fore.WHITE + Back.BLACK + Style.DIM,
    Fore.WHITE + Back.BLACK + Style.DIM,
    Fore.WHITE + Back.BLACK + Style.DIM,
    Fore.CYAN  + Back.BLACK + Style.DIM,
    Fore.CYAN  + Back.BLACK + Style.DIM,
    Fore.CYAN  + Back.BLACK + Style.DIM,
    Fore.CYAN  + Back.BLACK + Style.NORMAL,
    Fore.CYAN  + Back.BLACK + Style.NORMAL,
    Fore.CYAN  + Back.BLACK + Style.BRIGHT
]
CHARS = ['o','◦','•','☣','⦾','⦿','❅','❆','☢','❄']

# Display the grid, all pretty and stuff
def display(grid):
    os.system('clear')

    for _ in range(5):
        print()

    for line in grid:
        print(' ' * 10, end='')

        for x in line:
            print(COLOURS[x] + CHARS[x], end='')

        print(Style.RESET_ALL)

    sleep(0.05)

grid = [[int(i) for i in line] for line in get_input_lines(11)]
HEIGHT = len(grid)
WIDTH = len(grid[0])

ADJACENT = [(i, j) for i in range(-1,2) for j in range(-1,2) if i != 0 or j != 0]

def get_adjacent(i, j):
    return [(i+di, j+dj) for di, dj in ADJACENT if 0 <= (i+di) < HEIGHT and 0 <= (j+dj) < WIDTH]

def increment(grid, i, j, flashing):
    grid[i][j] += 1
    if grid[i][j] == 10:
        flashing.append((i,j))

def step(grid):
    flashing = []

    for i in range(HEIGHT):
        for j in range(WIDTH):
            increment(grid, i, j, flashing)

    flashed = set()
    while flashing:
        i, j = flashing.pop()
        if (i,j) in flashed:
            next
        flashed.add((i,j))

        grid[i][j] = 0
        for adjacent in get_adjacent(i, j):
            if adjacent not in flashed:
                increment(grid, *adjacent, flashing)

    display(grid)
    return len(flashed)

display(grid)
part_1 = sum(step(grid) for _ in range(100))

part_2 = 101
while step(grid) != WIDTH * HEIGHT:
    part_2 += 1

print("Part 1:")
print(part_1)
print("Part 2:")
print(part_2)
