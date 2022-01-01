import pytest
import context

import day17

@pytest.fixture
def sample_input():
    return 'target area: x=20..30, y=-10..-5'

@pytest.fixture
def sample_area(sample_input):
    return day17.parse(sample_input)

def test_parse(sample_input):
    assert day17.parse(sample_input) == ((20,30), (-10,-5))

def test_limits(sample_area):
    assert day17.limits(sample_area) == ((6,15), (-4,9))

def test_max_height(sample_area):
    assert day17.max_height(sample_area) == 45

def test_valid_trajectory(sample_area):
    assert day17.valid_trajectory(sample_area, 6, 9)
    assert day17.valid_trajectory(sample_area, 9, 0)
    assert day17.valid_trajectory(sample_area, 6, 3)
    assert day17.valid_trajectory(sample_area, 7, 2)

    assert not day17.valid_trajectory(sample_area, 17, -4)

def test_all_trajectories(sample_area):
    trajectories = day17.all_trajectories(sample_area)
    assert len(trajectories) == 112

    trajectories = day17.all_trajectories(day17.parse('target area: x=85..145, y=-163..-108'))
    assert len(trajectories) == 5644
