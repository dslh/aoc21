import pytest

import context
import day1

@pytest.fixture
def sample():
    return [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263
    ]

def test_windowed():
    assert list(day1.windowed(range(4))) == [[0,1], [1,2], [2,3]]
    assert list(day1.windowed(range(4),3)) == [[0,1,2], [1,2,3]]

def test_part_one(sample):
    assert day1.count_increases(sample) == 7

def test_part_two(sample):
    assert day1.count_increases(sample, 3) == 5

