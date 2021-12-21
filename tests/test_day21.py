import pytest
import context

from day21 import deterministic_die, play

def test_deterministic_die():
    die = iter(deterministic_die())
    assert next(die) == 1
    assert next(die) == 2
    assert next(die) == 3
    assert next(die) == 4

    for i in range(5,100):
        assert next(die) == i

    assert next(die) == 100
    assert next(die) == 1
    assert next(die) == 2

def test_part_one():
    assert play([4,8], iter(deterministic_die())) == 739785
