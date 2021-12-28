import pytest
import context

from day25 import run, parse

def test_parse():
    lines = [
        '...>...',
        '.......',
        '......>',
        'v.....>',
        '......>',
        '.......',
        '..vvv..'
    ]

    east, south, limits = parse(lines)
    assert east == {(3,0), (6,2), (6,3), (6,4)}
    assert south == {(0,3), (2,6), (3,6), (4,6)}
    assert limits == (7,7)

def test_run():
    lines = [
        'v...>>.vv>',
        '.vv>>.vv..',
        '>>.>v>...v',
        '>>v>>.>.v.',
        'v>v.vv.v..',
        '>.>>..v...',
        '.vv..>.>v.',
        'v.v..>>v.v',
        '....v..v.>'
    ]

    east, south, limits = parse(lines)

    step, new_east, new_south = run(east, south, limits)
    assert step == 58
