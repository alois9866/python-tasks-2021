import copy
from typing import List

import pytest

import fifteen


def test_neighbors():
    assert fifteen.neighbors(0, 0) == [(1, 0), (0, 1)]
    assert fifteen.neighbors(0, 3) == [(1, 3), (0, 2)]
    assert fifteen.neighbors(3, 0) == [(2, 0), (3, 1)]
    assert fifteen.neighbors(3, 3) == [(2, 3), (3, 2)]
    assert fifteen.neighbors(2, 2) == [(1, 2), (3, 2), (2, 1), (2, 3)]


def test_fifteen():
    f = fifteen.Fifteen()
    numbers = []
    for x in range(4):
        for y in range(4):
            numbers.append(f.state[x][y])
    for n in range(16):
        assert n in numbers


TARGET = (2, 2)


def swap(game: List[List[int]], x: int, y: int):
    game[x][y], game[TARGET[0]][TARGET[1]] = game[TARGET[0]][TARGET[1]], game[x][y]


def test_hit():
    f = fifteen.Fifteen()

    # Prepare.
    f.state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    swap(f.state, 3, 3)

    # Hit outside of the game.
    with pytest.raises(ValueError):
        f.hit(-1, 2)
    with pytest.raises(ValueError):
        f.hit(2, -1)
    with pytest.raises(ValueError):
        f.hit(5, 2)
    with pytest.raises(ValueError):
        f.hit(2, 5)

    # Hit away from zero.
    previous_state = copy.deepcopy(f.state)
    f.hit(0, 0)
    assert f.state == previous_state

    # Hit zero.
    previous_state = copy.deepcopy(f.state)
    f.hit(2, 2)
    assert f.state == previous_state

    # Hit near zero.
    previous_state = copy.deepcopy(f.state)
    f.hit(1, 2)
    assert f.state != previous_state
    assert f.state[1][2] == 0
    assert f.state[2][2] == previous_state[1][2]
