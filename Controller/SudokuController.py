
class SudokuController:

    _sudokuModel = None
    _sudokuRules = None
    _probabilityReducer = None
    _solved = False

    def __init__(self, sudokuModel, sudokuRules, probabilityReducer):

        self._sudokuModel = sudokuModel
        self._sudokuRules = sudokuRules
        self._probabilityReducer = probabilityReducer

    def solveSudoku(self):
        if self._solved:
            return

        # print(self._sudokuModel.getBoard())
        # print("Board", self._sudokuModel.getBoard())
        self.generatePossibilities()

        possibilities = self._sudokuModel.getPossibilities()
        # print("Base Possibilities")
        # for row in possibilities:
        #     print(row)
        self.reducePossibilities()

        # print("Probs", self._sudokuModel.getPossibilities())
        # print()
        wasUpdated = self.updateBoard()

        if wasUpdated:
            self.solveSudoku()

    def getIterations(self):
        return self._iterations

    def isSolved(self):
        return self._solved

    def generatePossibilities(self):
        self._sudokuModel.setPossibilities(self._sudokuRules.generatePossibilities(
            self._sudokuModel.getBoard()))

        # board = self._sudokuModel.getBoard()
        # possibilities = []
        # for row in board:
        #     newRow = []
        #     for column in row:
        #         if len(column) == 1:
        #             newRow.append({column})
        #         else:
        #             newRow.append(
        #                 {'1', '2', '3', '4', '5', '6', '7', '8', '9'})
        #     possibilities.append(newRow.copy())
        # print(possibilities)
        # self._sudokuModel.setPossibilities(possibilities)

    def reducePossibilities(self):
        possibilities = self._sudokuModel.getPossibilities()
        self._sudokuModel.setPossibilities(
            self._probabilityReducer.reducePossibilities(possibilities))

    def updateBoard(self):
        boardModified = False
        boardSize = self._sudokuModel.getBoardSize()
        for i in range(boardSize):
            for j in range(boardSize):
                position = (i, j)
                if self._sudokuModel.getValue(position) != "":
                    continue

                probabilites = set(
                    self._sudokuModel.getPositionPossibilities(position))

                if len(probabilites) > 1:
                    continue

                for value in probabilites:
                    self._sudokuModel.setValue(position, value)
                    boardModified = True

        return boardModified


def main():
    pass


if __name__ == '__main__':
    main()
