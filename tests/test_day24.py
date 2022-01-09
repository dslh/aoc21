import pytest
import context

from day24 import Program, run

from os.path import join, dirname

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

@pytest.fixture
def input_program():
    filename = join(dirname(__file__), 'fixtures/24.input')
    return open(filename, 'r').read().rstrip().rsplit('\n')

@pytest.fixture
def sample_sequences():
    return [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 2, 3, 5, 8, 7, 6, 1, 4, 9, 5, 2, 1, 7],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [1, 2, 1, 2, 9, 3, 8, 5, 7, 6, 1, 3, 2, 8],
        [9, 1, 2, 3, 8, 5, 7, 6, 2, 3, 8, 7, 5, 6],
        [2, 3, 8, 5, 7, 9, 1, 5, 9, 2, 8, 7, 3, 7],
        [5, 6, 2, 7, 8, 1, 9, 3, 5, 8, 1, 6, 2, 3]
    ]

def test_run(input_program, sample_sequences):
    program = Program(input_program)

    for seq in sample_sequences:
        assert program.run(seq)['z'] == run(seq)
