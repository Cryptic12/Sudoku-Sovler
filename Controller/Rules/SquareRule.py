import math


class SquareRule:

    _squareSize = 3

    def __init__(self, squareSize):
        self._squareSize = squareSize

    def isAllowed(self, board, value, position):
        row, column = position

        rowBase = self._baseCalculator(row)
        columnBase = self._baseCalculator(column)

        for i in range(0, self._squareSize):
            curRow = rowBase + i
            for j in range(0, self._squareSize):
                curColumn = columnBase + j

                if board[curRow][curColumn] == value:
                    return False

        return True

    def getSquarePositions(self, square: int):
        positions = []
        rowBase = math.floor(square / self._squareSize) * self._squareSize
        columnBase = (square % self._squareSize) * self._squareSize
        for row in range(self._squareSize):
            for column in range(self._squareSize):
                positions.append((rowBase + row, columnBase + column))
        # print(positions)
        return positions

    def getAllSquarePositions(self):
        squares = []
        for square in range(9):
            squares.append(self.getSquarePositions(square))
        return squares

    def getAffectedPositions(self, position):
        row, column = position
        square = math.floor(row / self._squareSize) * 3 + \
            math.floor(column / self._squareSize)
        affectedPositions = set(self.getSquarePositions(square))
        affectedPositions.remove(position)
        return affectedPositions

    def _baseCalculator(self, base):
        return math.floor(base / self._squareSize) * self._squareSize
