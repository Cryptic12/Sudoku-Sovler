import math
from typing import Set

from Model.SudokuEvents import SudokuEvents
from Other.Subscriber import Subscriber


class SudokuModel:

    _board = None
    _possibilities = None
    _board_size = 9
    _square_size = 3
    _subscribers = []
    _subscriber_ids = set()
    _max_subs = 100

    def __init__(self, board=None, board_size=9, square_size=3):

        self._board_size = board_size
        self._square_size = square_size

        if board is None:
            self.init_empty_board()
            return

        self.verify_board(board)
        self._board = board

    def verify_board(self, board):

        if len(board) != self._board_size:
            raise ValueError(
                f'Row count not equal to board size. Expected {self._board_size} recieved {len(board)}')

        for i in range(0, self._board_size):
            if (len(board[i]) != self._board_size):
                raise ValueError(
                    f'Column count in row {i + 1} not equal to board size. Expected {self._board_size} recieved {len(board)}')

    def init_empty_board(self):
        board = []
        row = []
        for i in range(0, self._board_size):
            row.append('')

        for i in range(0, self._board_size):
            board.append(row)

        self._board = board

    def _notify(self, event):
        for subscriber in self._subscribers:
            subscriber.notify(event)

    def notify(self, event):
        self._notify(event)

    def subscribe(self, subscriber):
        id = 0
        while id < self._max_subs:
            if id in self._subscriber_ids:
                id += 1
            else:
                self._subscriber_ids.add(id)
                subscriber.set_id(id)
                self._subscribers.append(subscriber)
                return subscriber

    def unsubscribe(self, id):
        if (id in self._subscriber_ids):
            for i in range(0, len(self._subscribers)):
                subscriber = self._subscribers[i]
                if (subscriber.get_id() == id):
                    self._subscribers.pop(i)
                    return True

        return False

    def get_board(self):
        return self._board

    def get_board_size(self):
        return self._board_size

    def get_row(self, row):
        return self._board[row]

    def get_column(self, column):
        values = []
        for i in range(0, self._board_size):
            values.append(self._board[i][column])

        return values

    def get_square(self, square):
        to_return = []
        column_pos = math.floor(square / self._square_size) * self._square_size
        row_pos = (square % self._square_size) * self._square_size
        board = self._board
        for x in range(column_pos, column_pos + self._square_size):
            curRow = board[x]
            for y in range(row_pos, row_pos + self._square_size):
                value = curRow[y]
                to_return.append(value)
        return to_return

    def get_value(self, position):
        row, column = position
        return self._board[row][column]

    def set_value(self, position, value):
        row, column = position
        self._board[row][column] = value
        event = {"event": SudokuEvents.VALUE_UPDATE,
                 "position": position,
                 "value": value}
        self._notify(event)

    def get_possibilities(self):
        return self._possibilities

    def set_possibilities(self, possibilities):
        self._possibilities = possibilities

    def get_position_possibilities(self, position):
        row, column = position
        return self._possibilities[row][column]

    def set_position_possibilities(self, position, possibility):
        row, column = position
        self._possibilities[row][column] = possibility


def test_func():
    print("I have been notified")


if __name__ == '__main__':
    sudoku = SudokuModel()
    subscriber = Subscriber(test_func)

    subscriber = sudoku.subscribe(subscriber)

    print(sudoku.get_board())

    sudoku.notify()
    print(sudoku.unsubscribe(subscriber.get_id()))
    sudoku.notify()
