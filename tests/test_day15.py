import pytest

import context
from day15 import Seeker

@python.fixture
def sample_map():
    string = """
        1163751742
        1381373672
        2136511328
        3694931569
        7463417111
        1319128137
        1359912421
        3125421639
        1293138521
        2311944581
    """

    return [[int(c) for c in line.strip()] for line in string.strip().split('\n')]

def sample_path():
    return [
        (0,0),
        (1,0),
        (2,0),
        (2,1),
        (2,2),
        (2,3),
        (2,4),
        (2,5),
        (2,6),
        (3,6),
        (3,7),
        (4,7),
        (5,7),
        (5,8),
        (6,8),
        (7,8),
        (8,8),
        (8,9),
        (9,9)
    ]

def test_seek(sample_map, sample_path):
    seeker = Seeker(sample_map)
    assert seeker.seek((0,0),(9,9)) == (40, sample_path)
