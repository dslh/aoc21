#!/usr/bin/env python3

from get_aoc import get_input_lines

# Allows me to refer to a coordinate pair as coord.x and coord.y
class Coord:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"{self.x},{self.y}"

    # Converts a coord into a single, semi-random number.
    # Required to use a coord as a dictionary key
    def __hash__(self):
        return hash((self.x, self.y))

    # Compare two coordinate objects to see if they are the same.
    # This method gets called if you write `a == b`, where `a` is a Coord.
    # Also needed to use a coord as a dictionary key
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# Unordered range. Like range(), but:
# - start and end can be given in either order
# - end is included in the range
def urange(start, end):
    direction = 1 if end > start else -1
    return range(start, end + direction, direction)

# A line of vents, as described in the input
class Line:
    # Takes a line of input and creates a new Line object
    def __init__(self, line):
        self.a, self.b = [Coord(*n.split(',')) for n in line.split(' -> ')]

    def __str__(self):
        return f"{self.a} -> {self.b}"

    def vertical(self):
        return self.a.x == self.b.x

    def horizontal(self):
        return self.a.y == self.b.y

    # Diagonal lines are straight too, but you know what I mean
    def straight(self):
        return self.horizontal() or self.vertical()

    # Generator function, allowing us to iterate over the points in the line
    def coords(self):
        if self.horizontal():
            for x in urange(self.a.x, self.b.x):
                yield Coord(x, self.a.y)

        elif self.vertical():
            for y in urange(self.a.y, self.b.y):
                yield Coord(self.a.x, y)

        else: # Guaranteed diagonal
            xr = iter(urange(self.a.x, self.b.x))
            yr = iter(urange(self.a.y, self.b.y))

            try:
                while True:
                    yield Coord(next(xr), next(yr))
            except StopIteration:
                return

lines = [Line(line) for line in get_input_lines(5)]

def height_map(lines):
    sea_floor = dict()
    for line in lines:
        for coord in line.coords():
            sea_floor[coord] = sea_floor.get(coord, 0) + 1

    return sea_floor

print("Part 1:")

straight_lines = [line for line in lines if line.straight()]
print(sum(height > 1 for height in height_map(straight_lines).values()))

print("Part 2:")

print(sum(height > 1 for height in height_map(lines).values()))
