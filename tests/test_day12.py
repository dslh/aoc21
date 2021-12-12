import pytest

import context
from day12 import Caves

@pytest.fixture
def sample_one():
    return [
        'start-A',
        'start-b',
        'A-c',
        'A-b',
        'b-d',
        'A-end',
        'b-end'
    ]

@pytest.fixture
def sample_two():
    return [
        'dc-end',
        'HN-start',
        'start-kj',
        'dc-start',
        'dc-HN',
        'LN-dc',
        'HN-end',
        'kj-sa',
        'kj-HN',
        'kj-dc'
    ]

@pytest.fixture
def sample_three():
    return [
        'fs-end',
        'he-DX',
        'fs-he',
        'start-DX',
        'pj-DX',
        'end-zg',
        'zg-sl',
        'zg-pj',
        'pj-he',
        'RW-he',
        'fs-DX',
        'pj-RW',
        'zg-RW',
        'start-pj',
        'he-WI',
        'zg-he',
        'pj-fs',
        'start-RW'
    ]

def test_init(sample_one):
    caves = Caves(sample_one)
    assert caves.links['start'] == {'A', 'b'}
    assert caves.links['A'] == {'start', 'end', 'c', 'b'}
    assert caves.links['b'] == {'start', 'end', 'A', 'd'}
    assert caves.links['c'] == {'A'}
    assert caves.links['d'] == {'b'}

def test_all_paths(sample_one, sample_two, sample_three):
    assert len(Caves(sample_one).all_paths()) == 10
    assert len(Caves(sample_two).all_paths()) == 19
    assert len(Caves(sample_three).all_paths()) == 226
