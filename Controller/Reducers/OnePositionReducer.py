
import math


class OnePositionReducer:
    """ Reduces posibilities by identifying positions in a given row/column/square that is the only position in the given row/column/square where it can be placed """

    def __init__(self, boardSize, squareSize, rules):
        self._boardSize = boardSize
        self._squareSize = squareSize
        self._rules = rules

    def identifySingleValues(self, possibilities):

        valueCounts = dict()
        for possibility in possibilities:
            for value in possibility:
                count = valueCounts.get(value)
                if count == None:
                    valueCounts[value] = 1
                else:
                    valueCounts[value] = count + 1

        singleValues = []

        for key in valueCounts:
            if valueCounts[key] == 1:
                singleValues.append(key)

        return singleValues

    def reduce(self, possibilities):
        possibilities = self.reduceByRow(possibilities)
        possibilities = self.reduceByColumn(possibilities)
        possibilities = self.reduceBySquare(possibilities)

        return possibilities

    def reduceByRow(self, possibilities):
        changes = []
        for row in range(self._boardSize):
            curRow = possibilities[row].copy()
            singleValues = self.identifySingleValues(curRow)

            if len(singleValues) == 0:
                continue

            for column in range(self._boardSize):
                for value in singleValues:
                    if value in possibilities[row][column] and len(possibilities[row][column]) > 1:
                        possibilities[row][column] = set(value)
                        change = ((row, column), value)
                        changes.append(change)

        if len(changes) > 0:
            print("Row", changes)
            possibilities = self._updateAffectedPositions(
                possibilities, changes)

        return possibilities

    def reduceByColumn(self, possibilities):
        changes = []
        for column in range(self._boardSize):
            curColumn = []
            for row in range(self._boardSize):
                curColumn.append(possibilities[row][column])

            singleValues = self.identifySingleValues(curColumn)

            if len(singleValues) == 0:
                continue

            for row in range(self._boardSize):
                for value in singleValues:
                    if value in possibilities[row][column] and len(possibilities[row][column]) > 1:
                        possibilities[row][column] = set(value)
                        change = ((row, column), value)
                        changes.append(change)

        if len(changes) > 0:
            print("Column", changes)
            possibilities = self._updateAffectedPositions(
                possibilities, changes)

        return possibilities

    def reduceBySquare(self, possibilities):

        SQUARE_COUNT = int(self._boardSize / self._squareSize) ** 2
        changes = []

        for square in range(0, SQUARE_COUNT):

            rowBase = (square % self._squareSize) * self._squareSize
            columnBase = math.floor(
                square / self._squareSize) * self._squareSize

            squarePossibilities = []
            for row in range(self._squareSize):
                curRow = rowBase + row
                for column in range(self._squareSize):
                    curColumn = columnBase + column
                    squarePossibilities.append(
                        possibilities[curRow][curColumn])

            singleValues = self.identifySingleValues(squarePossibilities)

            # TODO the below code is roughly duplicated throughout the 3 functions. Should find a way to remove
            if len(singleValues) == 0:
                continue

            for row in range(0, self._squareSize):
                curRow = rowBase + row
                for column in range(0, self._squareSize):
                    curColumn = columnBase + column
                    for value in singleValues:
                        if value in possibilities[curRow][curColumn] and len(possibilities[curRow][curColumn]) > 1:
                            possibilities[curRow][curColumn] = set(value)
                            change = ((curRow, curColumn), value)
                            changes.append(change)

        if len(changes) > 0:
            print("Square", changes)
            possibilities = self._updateAffectedPositions(
                possibilities, changes)

        return possibilities

    def _updateAffectedPositions(self, possibilities, changes):

        newChanges = []

        for change in changes:
            position, value = change
            affectedPositions = set()

            for rule in self._rules:
                affectedPositions = affectedPositions.union(
                    rule.getAffectedPositions(position))

            for affectPosition in affectedPositions:
                row, column = affectPosition

                if value in possibilities[row][column] and len(possibilities[row][column]) > 1:
                    curPossibilities = possibilities[row][column].copy()
                    curPossibilities.remove(
                        value)
                    possibilities[row][column] = curPossibilities

                    if len(curPossibilities) == 1:
                        newChanges.append(((row, column), next(
                            iter(possibilities[row][column]))))

        if len(newChanges) > 0:
            print(f"Extras: {newChanges} for {changes}")
            for row in possibilities:
                print(row)
            possibilities = self._updateAffectedPositions(
                possibilities, newChanges)

        return possibilities
