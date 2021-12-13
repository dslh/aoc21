import pytest

import context
from day13 import Sheet, parse_fold

from inspect import cleandoc

@pytest.fixture
def sample_dots():
    return [
        '6,10',
        '0,14',
        '9,10',
        '0,3',
        '10,4',
        '4,11',
        '6,0',
        '6,12',
        '4,1',
        '0,13',
        '10,12',
        '3,4',
        '3,0',
        '8,4',
        '1,10',
        '2,14',
        '8,10',
        '9,0'
    ]

def test_init_sheet():
    sheet = Sheet(['1,2', '3,4'])
    assert sheet.dots == {(1,2), (3,4)}

def test_fold():
    sheet = Sheet(["1,1", "9,1", "9,9"])

    sheet.fold('x', 5)
    assert sheet.dots == {(1,1), (1,9)}

    sheet.fold('y', 5)
    assert sheet.dots == {(1,1)}

def test_part_one(sample_dots):
    sheet = Sheet(sample_dots)
    assert len(sheet.dots) == len(sample_dots)

    sheet.fold('y', 7)
    assert len(sheet.dots) == 17
    assert (0,0) in sheet.dots
    assert (0,14) not in sheet.dots

    assert (0,1) in sheet.dots
    assert (0,13) not in sheet.dots

def test_parse_fold():
    assert parse_fold('fold along y=7') == ('y', 7)
    assert parse_fold('fold along x=5') == ('x', 5)

def test_sheet_str(sample_dots):
    sheet = Sheet(sample_dots)

    initial = """\
        ...#..#..#.
        ....#......
        ...........
        #..........
        ...#....#.#
        ...........
        ...........
        ...........
        ...........
        ...........
        .#....#.##.
        ....#......
        ......#...#
        #..........
        #.#........
    """

    assert str(sheet) == cleandoc(initial)

    first = """\
        #.##..#..#.
        #...#......
        ......#...#
        #...#......
        .#.#..#.###
    """
    sheet.fold('y', 7)
    assert str(sheet) == cleandoc(first)

    second = """\
        #####
        #...#
        #...#
        #...#
        #####
    """
    sheet.fold('x', 5)
    assert str(sheet) == cleandoc(second)
