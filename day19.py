#!/usr/bin/env python3

from itertools import combinations

def distance(a, b):
    # Leaving out the sqrt to avoid floating point errors
    return sum((a[i] - b[i]) ** 2 for i in range(3))

def diff(a, b):
    return tuple(a[i] - b[i] for i in range(3))

def add(a, b):
    return tuple(a[i] + b[i] for i in range(3))

def rotate_x(coords):
    return [(x,z,-y) for x,y,z in coords]

def rotate_z(coords):
    return [(y,-x,z) for x,y,z in coords]

def rotations(coords):
    yield coords
    for _ in range(3):
        coords = rotate_z(coords)
        yield coords

def orientations(coords):
    yield from rotations(coords)

    side = [(z,y,-x) for x,y,z in coords]
    yield from rotations(side)
    side = [(-z,y,x) for x,y,z in coords]
    yield from rotations(side)

    coords = rotate_x(coords)
    yield from rotations(coords)
    coords = rotate_x(coords)
    yield from rotations(coords)
    coords = rotate_x(coords)
    yield from rotations(coords)

class Field:
    def __init__(self, chunk):
        self.centre = (0,0,0)
        self.coords = [
            tuple(int(x) for x in line.split(','))
            for line in chunk.split('\n')[1:]
        ]
        self.coord_index = range(len(self.coords)) # It gets used a lot

        # We can eliminate most non-intersecting fields by comparing distances
        # between points within the fields. If there are 12 identical points in
        # the two fields, then there will be 11+10+9+... = 66 matching distances
        # between points
        self.distances = set()

        # We can then identify matching points using a similar method. If two
        # points share 11 distances then they are probably the same point.
        self.coord_dists = [set() for _ in self.coord_index]

        for i,j in combinations(self.coord_index, 2):
            dist = distance(self.coords[i],self.coords[j])
            self.distances.add(dist)
            self.coord_dists[i].add(dist)
            self.coord_dists[j].add(dist)

    def orientations(self):
        yield from orientations(self.coords)

    def overlay(self, other):
        common_dists = self.distances & other.distances
        if len(common_dists) < 66:
            return False

        # Find common points from self
        # We will reorient the entire field so we just want the indices
        common_indices = [i for i in self.coord_index if len(self.coord_dists[i] & common_dists) >= 11]

        # Find common points from other
        # This is our target so we keep a set for easy comparison
        common_coords = {other.coords[i] for i in other.coord_index if len(other.coord_dists[i] & common_dists) >= 11}

        # Work out a match between two points
        ref_index = common_indices[0]
        ref_coord = other.coords[next(i for i in other.coord_index if len(other.coord_dists[i] & self.coord_dists[ref_index]) >= 11)]

        for coords in self.orientations():
            d = diff(ref_coord, coords[ref_index])
            coords = [add(c, d) for c in coords]
            if set(coords).issuperset(common_coords):
                self.centre = d
                self.coords = coords
                return True

        raise RuntimeError

def overlay_all(fields):
    overlaid = [fields[0]]
    fields = fields[1:]

    while fields:
        field = next(f for f in fields if any(f.overlay(o) for o in overlaid))
        fields.remove(field)
        overlaid.append(field)

if __name__ == '__main__':
    from get_aoc import get_input_chunks
    fields = [Field(chunk) for chunk in get_input_chunks(19)]

    print('Part 1:')
    overlay_all(fields)
    coords = set(coord for field in fields for coord in field.coords)
    print(len(coords))
