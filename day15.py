#!/usr/bin/env python3

from queue import PriorityQueue, LifoQueue, Queue

import box_chars
import os
import time

ADJACENCY = [(0,1),(1,0),(-1,0),(0,-1)]

class Seeker:
    def __init__(self, grid, animate=False):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.animate = animate

    def cost(self, pos):
        i, j = pos
        return self.grid[i][j]

    def neighbours(self, pos):
        i, j = pos
        return [(i+k,j+l) for k,l in ADJACENCY if 0 <= i+k < self.height and 0 <= j+l < self.width]

    def visit(self, cost, pos, prev):
        i, j = pos
        self.visited[i][j] = (cost, prev)

    def path(self, pos):
        path = []

        while pos:
            path.append(pos)
            i, j = pos
            if pos == (0,0):
                break
            _, pos = self.visited[i][j]

        return path[::-1]

    def seek(self, start, end):
        self.visited = [[None] * self.width for _ in range(self.height)]
        self.visits = PriorityQueue()

        for pos in self.neighbours(start):
            self.visits.put((self.cost(pos), pos, start))

        self.visit(0, start, None)

        while not self.visits.empty():
            cost, pos, prev = self.visits.get()
            visited = self.visited[pos[0]][pos[1]]
            if visited and visited[0] <= cost:
                continue

            self.visit(cost, pos, prev)

            if self.animate:
                os.system('clear')
                box_chars.show(self, pos, start, end)
                time.sleep(0.05)

            for neigh in self.neighbours(pos):
                visited = self.visited[neigh[0]][neigh[1]]
                if not visited or visited[0] > cost + self.cost(neigh):
                    self.visits.put((cost + self.cost(neigh), neigh, pos))

        cost, _ = self.visited[end[0]][end[1]]

        if self.animate:
            os.system('clear')
        box_chars.show(self, end, start, end)
        return cost, self.path(end)

def expand(grid, scale=5):
    def inc(value, amount):
        return (value + amount - 1) % 9 + 1

    return [
        [inc(n, i + j) for i in range(scale) for n in line]
        for j in range(scale) for line in grid
    ]

if __name__ == '__main__':
    from get_aoc import get_input_lines
    grid = [[int(c) for c in line] for line in get_input_lines(15)]

    seeker = Seeker(grid)
    end = (seeker.height - 1, seeker.width - 1)
    cost, path = seeker.seek((0,0), end)

    print("Part 1:")
    print(cost)

    print("Part 2:")
    seeker = Seeker(expand(grid), True)
    end = (seeker.height - 1, seeker.width - 1)
    cost, path = seeker.seek((0,0), end)
    print(cost)
