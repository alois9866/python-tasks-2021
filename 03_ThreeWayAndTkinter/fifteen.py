import random
from typing import List


def neighbors(x: int, y: int):
    default = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return list(filter(lambda p: 0 <= p[0] <= 3 and 0 <= p[1] <= 3, default))


class Fifteen:
    """Represents a game of fifteen."""

    winning_state = [[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 0]]

    state: List[List[int]]  # 4 by 4, origin point is in upper left corner.

    def __init__(self):
        """Creates random game of fifteen."""
        self.reset()

    def reset(self):
        numbers = list(range(0, 15 + 1))
        random.shuffle(numbers)

        self.state = [[0] * 4 for i in range(4)]
        for x in range(4):
            for y in range(4):
                self.state[x][y] = numbers[x * 4 + y]

    def won(self) -> bool:
        return self.state == self.winning_state

    def hit(self, x: int, y: int):
        """Tries to move the piece at (x, y) to the adjacent free piece, if possible."""
        if x < 0 or x > 3 or y < 0 or y > 3:
            raise ValueError(f'unable to hit square with coordinates ({x}, {y})')

        if self.state[x][y] == 0:
            return

        for (nx, ny) in neighbors(x, y):
            if self.state[nx][ny] == 0:
                self.state[nx][ny] = self.state[x][y]
                self.state[x][y] = 0
                break
