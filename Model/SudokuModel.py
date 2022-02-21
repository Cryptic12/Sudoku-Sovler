from ast import Pass
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

    def __init__(self, board_size=9, square_size=3):

        self._board_size = board_size
        self._square_size = square_size
        self.init_empty_board()

    # Loads the board into the model
    def load_board(self, board):
        self.verify_board(board)
        for row in range(0, self._board_size):
            for column in range(0, self._board_size):
                self.set_value((row, column), board[row][column])

    # Checks that the board will work with the configured model
    def verify_board(self, board):

        if len(board) != self._board_size:
            raise ValueError(
                f'Row count not equal to board size. Expected {self._board_size} recieved {len(board)}')

        for i in range(0, self._board_size):
            if (len(board[i]) != self._board_size):
                raise ValueError(
                    f'Column count in row {i + 1} not equal to board size. Expected {self._board_size} recieved {len(board)}')

    # Sets up a empty board
    def init_empty_board(self):
        board = []
        row = []
        for _ in range(0, self._board_size):
            row.append('')

        for _ in range(0, self._board_size):
            board.append(row.copy())

        self._board = board

    # Notifies all subscribers of the event
    def _notify(self, event):
        for subscriber in self._subscribers:
            subscriber.notify(event)

    # Adds a subscriber to the model
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

    # Removes the given subscriber
    def unsubscribe(self, id):
        if (id in self._subscriber_ids):
            for i in range(0, len(self._subscribers)):
                subscriber = self._subscribers[i]
                if (subscriber.get_id() == id):
                    self._subscribers.pop(i)
                    return True

        return False

    # Returns the board
    def get_board(self):
        return self._board

    # Returns the board size
    def get_board_size(self):
        return self._board_size

    # Returns the value of the given position
    def get_value(self, position):
        row, column = position
        return self._board[row][column]

    # Sets the postiion to the given value
    def set_value(self, position, value):
        row, column = position
        self._board[row][column] = value
        event = {"event": SudokuEvents.VALUE_UPDATE,
                 "position": position,
                 "value": value}

        self._notify(event)

    # Returns the possibilities
    def get_possibilities(self):
        return self._possibilities

    # Set the possibilities
    def set_possibilities(self, possibilities):
        self._possibilities = possibilities

    # Get the possibilities for a given position
    def get_position_possibilities(self, position):
        row, column = position
        return self._possibilities[row][column]

    # Set the possibilities for a given position
    def set_position_possibilities(self, position, possibility):
        row, column = position
        self._possibilities[row][column] = possibility


def main():
    pass


if __name__ == '__main__':
    main()
