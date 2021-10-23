
class SudokuRules():

    _rules = []

    def __init__(self, rules):
        self._rules = rules

    def check(self, solvedValues, value, position):
        for rule in self._rules:
            if not rule.isAllowed(solvedValues, value, position):
                return False
        return True

    def generatePossibilities(self, board):
        possibilities = []
        boardSize = len(board)
        solvedPositions = []

        for x in range(boardSize):
            row = []
            for y in range(boardSize):
                allowedValues = set()
                if board[x][y] != "":
                    allowedValues.add(board[x][y])
                else:
                    for value in range(1, boardSize + 1):
                        value = str(value)
                        if self.check(board, value, (x, y)):
                            allowedValues.add(value)
                row.append(allowedValues)
                if len(allowedValues) == 1:
                    solvedPositions.append(((x, y), next(iter(allowedValues))))
            possibilities.append(row)

        possibilities = self._reduceBySolved(possibilities, solvedPositions)

        return possibilities

    def _reduceBySolved(self, possibilities, solvedPositions):
        newSolvedPositions = []
        for solvedPosition in solvedPositions:
            position, value = solvedPosition

            affectedPositions = self.affectedPositions(position)
            for affectedPosition in affectedPositions:
                row, column = affectedPosition
                if len(possibilities[row][column]) > 1 and value in possibilities[row][column]:
                    possibilities[row][column].remove(value)

                    if len(possibilities[row][column]) == 1:
                        newSolvedPositions.append(((row, column), next(
                            iter(possibilities[row][column]))))

        if len(newSolvedPositions) > 0:
            possibilities = self._reduceBySolved(
                possibilities, newSolvedPositions)

        return possibilities

    def affectedPositions(self, position):
        positions = set()
        for rule in self._rules:
            positions = positions.union(
                rule.getAffectedPositions(position))
        return positions
