#!/usr/bin/env python3

from get_aoc import get_input_lines

grid = [[int(i) for i in line] for line in get_input_lines(9)]
HEIGHT = len(grid)
WIDTH = len(grid[0])

def get_neighbours(i, j):
    neighbours = []
    if i > 0: neighbours.append((i - 1, j))
    if j > 0: neighbours.append((i, j - 1))
    if i < HEIGHT - 1: neighbours.append((i + 1, j))
    if j < WIDTH - 1: neighbours.append((i, j + 1))
    return neighbours

def get_values(grid, coords):
    return [grid[i][j] for i, j in coords]

def get_neighbour_values(grid, i, j):
    return get_values(grid, get_neighbours(i, j))

minima = [(i, j) for i in range(HEIGHT)
                 for j in range(WIDTH)
                 if grid[i][j] < min(get_neighbour_values(grid, i, j))]

print("Part 1:")
print(sum(get_values(grid, minima)) + len(minima))
