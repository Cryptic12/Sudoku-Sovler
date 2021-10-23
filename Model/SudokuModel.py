import math
from typing import Set

from Model.SudokuEvents import SudokuEvents
from Other.Subscriber import Subscriber


class SudokuModel:

    _board = None
    _possibilities = None
    _boardSize = 9
    _squareSize = 3
    _subscribers = []
    _subscriberIds = set()
    _maxSubs = 100

    def __init__(self, board=None, boardSize=9, squareSize=3):

        self._boardSize = boardSize
        self._squareSize = squareSize

        if board is None:
            self.initEmptyBoard()
            return

        self.verifyBoard(board)
        self._board = board

    def verifyBoard(self, board):

        if len(board) != self._boardSize:
            raise ValueError(
                f'Row count not equal to board size. Expected {self._boardSize} recieved {len(board)}')

        for i in range(0, self._boardSize):
            if (len(board[i]) != self._boardSize):
                raise ValueError(
                    f'Column count in row {i + 1} not equal to board size. Expected {self._boardSize} recieved {len(board)}')

        pass

    def initEmptyBoard(self):
        board = []
        row = []
        for i in range(0, self._boardSize):
            row.append('')

        for i in range(0, self._boardSize):
            board.append(row)

        self._board = board

    def __notify(self, event):
        for subscriber in self._subscribers:
            subscriber.notify(event)

    def notify(self, event):
        self.__notify(event)

    def subscribe(self, subscriber):
        id = 0
        while id < self._maxSubs:
            if id in self._subscriberIds:
                id += 1
            else:
                self._subscriberIds.add(id)
                subscriber.setId(id)
                self._subscribers.append(subscriber)
                return subscriber

    def unsubscribe(self, id):
        if (id in self._subscriberIds):
            for i in range(0, len(self._subscribers)):
                subscriber = self._subscribers[i]
                if (subscriber.getId() == id):
                    self._subscribers.pop(i)
                    return True

        return False

    def getBoard(self):
        return self._board

    def getBoardSize(self):
        return self._boardSize

    def getRow(self, row):
        return self._board[row]

    def getColumn(self, column):
        values = []
        for i in range(0, self._boardSize):
            values.append(self._board[i][column])

        return values

    def getSquare(self, square):
        toReturn = []
        columnPos = math.floor(square / self._squareSize) * self._squareSize
        rowPos = (square % self._squareSize) * self._squareSize
        board = self._board
        for x in range(columnPos, columnPos + self._squareSize):
            curRow = board[x]
            for y in range(rowPos, rowPos + self._squareSize):
                value = curRow[y]
                toReturn.append(value)
        return toReturn

    def getValue(self, position):
        row, column = position
        return self._board[row][column]

    def setValue(self, position, value):
        row, column = position
        self._board[row][column] = value
        event = {"event": SudokuEvents.VALUE_UPDATE,
                 "position": position,
                 "value": value}
        self.__notify(event)

    def getPossibilities(self):
        return self._possibilities

    def setPossibilities(self, possibilities):
        self._possibilities = possibilities

    def getPositionPossibilities(self, position):
        row, column = position
        return self._possibilities[row][column]

    def setPositionPossibilities(self, position, possibility):
        row, column = position
        self._possibilities[row][column] = possibility


def testFunc():
    print("I have been notified")


if __name__ == '__main__':
    sudoku = SudokuModel()
    subscriber = Subscriber(testFunc)

    subscriber = sudoku.subscribe(subscriber)

    print(sudoku.getBoard())

    sudoku.notify()
    print(sudoku.unsubscribe(subscriber.getId()))
    sudoku.notify()
