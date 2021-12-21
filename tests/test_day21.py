import pytest
import context

from day21 import play_deterministic, play_quantum

def test_part_one():
    assert play_deterministic([4,8]) == 739785

def test_part_two():
    assert play_quantum([4,8]) == (444356092776315, 341960390180808)
