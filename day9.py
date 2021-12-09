#!/usr/bin/env python3

from get_aoc import get_input_lines
from math import prod

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

def smoke_out(grid, i, j, visited=set()):
    if (i, j) in visited or grid[i][j] == 9:
        return 0

    visited.add((i, j))

    return 1 + sum(smoke_out(grid, i, j, visited) for i, j in get_neighbours(i, j))

basin_sizes = [smoke_out(grid, i, j) for i, j in minima]
basin_sizes.sort(reverse=True)

print("Part 2:")
print(prod(basin_sizes[:3]))

def smoke_up(grid, i, j):
    visited = set()
    to_visit = [(i, j)]
    while to_visit:
        i, j = to_visit.pop()
        visited.add((i, j))
        to_visit.extend((i, j) for i, j in get_neighbours(i, j)
                               if (i, j) not in visited
                               and grid[i][j] != 9)

    return len(visited)

basin_sizes = [smoke_up(grid, i, j) for i, j in minima]
basin_sizes.sort(reverse=True)

print("Part 2:")
print(prod(basin_sizes[:3]))
