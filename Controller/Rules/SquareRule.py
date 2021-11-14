import math


class SquareRule:

    square_size = 3

    def __init__(self, square_size):
        self.square_size = square_size

    def is_allowed(self, board, value, position):
        ROW, COLUMN = position

        ROW_BASE = self._base_calculator(ROW)
        COLUMN_BASE = self._base_calculator(COLUMN)

        for i in range(0, self.square_size):
            cur_row = ROW_BASE + i
            for j in range(0, self.square_size):
                cur_column = COLUMN_BASE + j

                if board[cur_row][cur_column] == value:
                    return False

        return True

    def get_positions(self, square: int):
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
        square = math.floor(ROW / self.square_size) * 3 + \
            math.floor(COLUMN / self.square_size)
        affected_positions = set(self.get_positions(square))
        affected_positions.remove(position)
        return affected_positions

    def _base_calculator(self, base):
        return math.floor(base / self.square_size) * self.square_size
