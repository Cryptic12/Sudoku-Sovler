from abc import ABC, abstractmethod
from typing import Protocol
import math


class Condition(Protocol):
    def check(positions, value) -> bool:
        ...


class Rule(ABC):

    def __init__(self, conditions):
        self.conditions = conditions

    # Check if the given value is allowed based on the rules conditions
    def is_allowed(self, board, value, position):
        positions_to_check = []
        for position in self.get_affected_positions(position):
            row, column = position
            positions_to_check.append(board[row][column])

        for condition in self.conditions:
            if not condition.check(positions_to_check, value):
                return False

        return True

    # Returns the given subset of positions from the sudoku
    @abstractmethod
    def get_positions(self, subset):
        ...

    # Returns each of the subsets of positions from the sudoku
    @abstractmethod
    def get_all_positions(self):
        ...

    # Returns other positions the belong to the same subset as the given position
    @abstractmethod
    def get_affected_positions(self, position):
        ...


class RowRule(Rule):
    def __init__(self, board_size, conditions):
        self.board_size = board_size
        super().__init__(conditions)

    def get_positions(self, row):
        positions = []
        for column in range(self.board_size):
            positions.append((row, column))

        return positions

    def get_all_positions(self):
        rows = []
        for row in range(self.board_size):
            rows.append(self.get_positions(row))
        return rows

    def get_affected_positions(self, position):
        row, _ = position
        affected_positions = set(self.get_positions(row))
        affected_positions.remove(position)
        return affected_positions


class ColumnRule(Rule):

    def __init__(self, board_size, conditions):
        self.board_size = board_size
        super().__init__(conditions)

    def get_positions(self, column):
        positions = []
        for row in range(self.board_size):
            positions.append((row, column))
        return positions

    def get_all_positions(self):
        columns = []
        for column in range(self.board_size):
            columns.append(self.get_positions(column))
        return columns

    def get_affected_positions(self, position):
        _, column = position
        affected_positions = set(self.get_positions(column))
        affected_positions.remove(position)
        return affected_positions


class SquareRule(Rule):

    def __init__(self, board_size, square_size, conditions):
        self.board_size = board_size
        self.square_size = square_size
        super().__init__(conditions)

    def get_positions(self, square):
        positions = []
        ROW_BASE = math.floor(square / self.square_size) * self.square_size
        COLUMN_BASE = (square % self.square_size) * self.square_size
        for row in range(self.square_size):
            for column in range(self.square_size):
                positions.append((ROW_BASE + row, COLUMN_BASE + column))

        return positions

    def get_all_positions(self):
        squares = []
        for square in range(9):
            squares.append(self.get_positions(square))
        return squares

    def get_affected_positions(self, position):
        ROW, COLUMN = position
        square = math.floor(ROW / self.square_size) * self.square_size + \
            math.floor(COLUMN / self.square_size)
        affected_positions = set(self.get_positions(square))
        affected_positions.remove(position)
        return affected_positions

    def _base_calculator(self, base):
        return math.floor(base / self.square_size) * self.square_size


def main():
    pass


if __name__ == '__main__':
    main()
