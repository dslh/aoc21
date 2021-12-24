import pytest
import context

from day24 import Program

@pytest.fixture
def negate():
    return ['inp x', 'mul x -1']

@pytest.fixture
def is_triple():
    return [
        'inp z',
        'inp x',
        'mul z 3',
        'eql z x'
    ]

@pytest.fixture
def save_bits():
    return [
        'inp w',
        'add z w',
        'mod z 2',
        'div w 2',
        'add y w',
        'mod y 2',
        'div w 2',
        'add x w',
        'mod x 2',
        'div w 2',
        'mod w 2'
    ]

def test_program(negate, is_triple, save_bits):
    p = Program(negate)
    r = p.run([5])
    assert r['x'] == -5
    r = p.run([1])
    assert r['x'] == -1

    p = Program(is_triple)
    r = p.run([9,3])
    assert r['z'] == 0
    r = p.run([3,9])
    assert r['z'] == 1

    p = Program(save_bits)
    r = p.run([0b1010])
    assert r['w'] == 1
    assert r['x'] == 0
    assert r['y'] == 1
    assert r['z'] == 0

    r = p.run([0b0101])
    assert r['w'] == 0
    assert r['x'] == 1
    assert r['y'] == 0
    assert r['z'] == 1

