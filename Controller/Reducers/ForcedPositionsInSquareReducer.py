from Controller.Rules.SquareRule import SquareRule


class ForcedPositionsInSquareReducer():
    """ Checks if all of the positions that contain a given value as a possibility are within the same square.
        If they are, we can remove that value as a possibility from all other positions within the square.
    """

    def __init__(self, squareRule):
        self._squareRule = squareRule

    def reduce(self, possibilities):
        possibilities = self.reduceByRow(possibilities)
        possibilities = self.reduceByColumn(possibilities)
        return possibilities

    def reduceByRow(self, possibilities):
        possibleValues = []
        possibilitiesSize = len(possibilities)
        for value in range(0, possibilitiesSize):
            possibleValues.append(str(value + 1))

        for value in possibleValues:
            for row in range(possibilitiesSize):
                positionsContainingValue = []
                for column in range(possibilitiesSize):
                    if value in possibilities[row][column]:
                        positionsContainingValue.append((row, column))

                #  Check if all positions containing the value are within the same square
                squarePositions = set()
                for positionContainingValue in positionsContainingValue:
                    if len(squarePositions) == 0:
                        squarePositions = self._squareRule.getAffectedPositions(
                            positionContainingValue)
                    else:
                        squarePositions = squarePositions.union(
                            self._squareRule.getAffectedPositions(positionContainingValue))

                if len(squarePositions) == possibilitiesSize:
                    for position in squarePositions:
                        squareRow, squarecolumn = position
                        if squareRow != row and value in possibilities[squareRow][squarecolumn]:
                            positionPossibilities = possibilities[squareRow][squarecolumn].copy(
                            )
                            positionPossibilities.remove(value)
                            possibilities[squareRow][squarecolumn] = positionPossibilities

        return possibilities

    def reduceByColumn(self, possibilities):
        possibleValues = []
        possibilitiesSize = len(possibilities)
        for value in range(0, possibilitiesSize):
            possibleValues.append(str(value + 1))

        for value in possibleValues:
            for column in range(possibilitiesSize):
                positionsContainingValue = []
                for row in range(possibilitiesSize):
                    if value in possibilities[row][column]:
                        positionsContainingValue.append((row, column))

                #  Check if all positions containing the value are within the same square
                squarePositions = set()
                for positionContainingValue in positionsContainingValue:
                    if len(squarePositions) == 0:
                        squarePositions = self._squareRule.getAffectedPositions(
                            positionContainingValue)
                    else:
                        squarePositions = squarePositions.union(
                            self._squareRule.getAffectedPositions(positionContainingValue))

                if len(squarePositions) == possibilitiesSize:
                    for position in squarePositions:
                        squareRow, squarecolumn = position
                        if squarecolumn != column and value in possibilities[squareRow][squarecolumn]:
                            positionPossibilities = possibilities[squareRow][squarecolumn].copy(
                            )
                            positionPossibilities.remove(value)
                            possibilities[squareRow][squarecolumn] = positionPossibilities

        return possibilities
