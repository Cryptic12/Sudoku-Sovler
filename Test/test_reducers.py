import unittest

from Controller.Reducers.OnePositionReducer import OnePositionReducer
from Controller.Reducers.ForcedPositionsReducer import ForcedPositionsReducer

from Test.SudokuTest import SudokuTest

BOARD_SIZE = 9
SQUARE_SIZE = 3


class TestOnePositionReducer(unittest.TestCase):

    def setUp(self):

        self.reducer = OnePositionReducer(BOARD_SIZE, SQUARE_SIZE)
        self.basePossibilities = [
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}]
        ]

        self.tests = []

        # Check that a single reduction is made
        self.tests.append(SudokuTest([{'1', '2'},
                                      {'1', '2'},
                                      {'3', '4'},
                                      {'3', '4'},
                                      {'5', '6'},
                                      {'6', '7'},
                                      {'6', '7'},
                                      {'8', '9'},
                                      {'8', '9'}], [4], [{'5'}]))

        # Check that multiple reductions are made
        self.tests.append(SudokuTest([{'1', '2', '3', '4', '5', '6', '7', '8'},
                                      {'1', '2', '3', '4', '5', '6', '7'},
                                      {'1', '2', '3', '4', '5', '6', '7'},
                                      {'1', '2', '3', '4', '5', '6', '7'},
                                      {'1', '2', '3', '4', '5', '6', '7'},
                                      {'1', '2', '3', '4', '5', '6', '7'},
                                      {'1', '2', '3', '4', '5', '6', '7'},
                                      {'1', '2', '3', '4', '5', '6', '7'},
                                      {'1', '2', '3', '4', '5', '6', '7', '9'}], [0, 8], [{'8'}, {'9'}]))

        # Check that no changes are made when no reductions are possible
        self.tests.append(SudokuTest([{'1', '2'},
                                      {'2', '3'},
                                      {'3', '4'},
                                      {'4', '5'},
                                      {'5', '6'},
                                      {'6', '7'},
                                      {'7', '8'},
                                      {'8', '9'},
                                      {'9', '1'}], [], []))

        self.tests.append(SudokuTest([{'9'},
                                {'3'},
                                {'1', '4'},
                                {'5', '6'},
                                {'5', '6'},
                                {'1', '7'},
                                {'2'},
                                {'8'},
                                {'1', '4', '7'}], [], []))

    def _assertMsg(self, row, column, modification, possibilities):
        messageParts = [
            f"\nRow: {row}, Column: {column} \nModification: {modification} \nPossibilities:"]
        for curRow in possibilities:
            messageParts.append(f"{curRow}")
        return "\n".join(messageParts)

    def test_row_mode(self):
        """ Tests that the single value is correctly detected in a row """
        MODIFIED_ROW = 2
        for modification in self.tests:
            self.basePossibilities[MODIFIED_ROW] = modification.startingValues
            reducedProbabilities = self.reducer.reduceByRow(
                self.basePossibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            for i in range(len(self.basePossibilities)):
                if i in modification.modifiedPositions:
                    self.assertSetEqual(
                        reducedProbabilities[MODIFIED_ROW][i], modification.modifiedValues[modification.modifiedPositions.index(i)], self._assertMsg(MODIFIED_ROW, i, modification, reducedProbabilities))
                else:
                    self.assertSetEqual(
                        reducedProbabilities[MODIFIED_ROW][i], self.basePossibilities[MODIFIED_ROW][i], self._assertMsg(MODIFIED_ROW, i, modification, reducedProbabilities))

    def test_column_mode(self):
        """ Tests that the single value is correctly detected in a column """
        MODIFIED_COLUMN = 2
        for modification in self.tests:
            for i in range(len(self.basePossibilities)):
                self.basePossibilities[i][MODIFIED_COLUMN] = modification.startingValues[i]

            reducedProbabilities = self.reducer.reduceByColumn(
                self.basePossibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            for i in range(len(self.basePossibilities)):
                if i in modification.modifiedPositions:
                    self.assertSetEqual(
                        reducedProbabilities[i][MODIFIED_COLUMN], modification.modifiedValues[modification.modifiedPositions.index(i)], self._assertMsg(i, MODIFIED_COLUMN, modification, reducedProbabilities))
                else:
                    self.assertSetEqual(
                        reducedProbabilities[i][MODIFIED_COLUMN], self.basePossibilities[i][MODIFIED_COLUMN], self._assertMsg(i, MODIFIED_COLUMN, modification, reducedProbabilities))

    def test_square_mode(self):
        """ Tests that the single value is correctly detected in a square """
        ROW_BASE = 3
        COLUMN_BASE = 3

        for modification in self.tests:

            modficationNumber = 0

            for i in range(3):
                for j in range(3):
                    row = ROW_BASE + i
                    column = COLUMN_BASE + j
                    self.basePossibilities[row][column] = modification.startingValues[modficationNumber]
                    modficationNumber += 1

            reducedProbabilities = self.reducer.reduceBySquare(
                self.basePossibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            # modficationNumber and checkNumber are used in the same way
            checkNumber = 0
            for i in range(3):
                for j in range(3):
                    row = ROW_BASE + i
                    column = COLUMN_BASE + j
                    if checkNumber in modification.modifiedPositions:
                        self.assertSetEqual(
                            reducedProbabilities[row][column], modification.modifiedValues[modification.modifiedPositions.index(checkNumber)], self._assertMsg(row, column, modification, reducedProbabilities))
                    else:
                        self.assertSetEqual(
                            reducedProbabilities[row][column], self.basePossibilities[row][column], self._assertMsg(row, column, modification, reducedProbabilities))
                    checkNumber += 1


class TestForcedPositionsReducer(unittest.TestCase):

    def setUp(self):

        self.reducer = ForcedPositionsReducer(BOARD_SIZE, SQUARE_SIZE)
        self.basePossibilities = [
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
            [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}]
        ]

        self.tests = []

        # Check that no changes are made when no reductions are possible
        self.tests.append(SudokuTest([{'1'},
                                      {'2'},
                                      {'3'},
                                      {'4'},
                                      {'5'},
                                      {'6'},
                                      {'7'},
                                      {'8'},
                                      {'9'}], [], []))

        # Check that the values are correctly removed for a permutation of 2 values
        self.tests.append(SudokuTest([{'1'},
                                      {'2'},
                                      {'3', '4', '9'},
                                      {'5', '6', '3'},
                                      {'5', '6', '4'},
                                      {'3', '4', '9'},
                                      {'7'},
                                      {'8'},
                                      {'3', '4', '9'}], [3, 4], [{'5', '6'}, {'5', '6'}]))

        # Check that the values are correctly removed for a permutation of 3 values
        self.tests.append(SudokuTest([{'1', '2', '3', '7'},
                                      {'1', '2', '3', '8'},
                                      {'1', '2', '3', '9'},
                                      {'4'},
                                      {'5'},
                                      {'6'},
                                      {'7', '8'},
                                      {'8', '9'},
                                      {'7', '9'}], [0, 1, 2], [{'1', '2', '3'}, {'1', '2', '3'}, {'1', '2', '3'}]))

        # Check that multiple permutation replacements can be handled at once
        self.tests.append(SudokuTest([{'1', '2', '3', '4'},
                                      {'1', '2', '3', '5'},
                                      {'1', '2', '3', '6'},
                                      {'4', '5'},
                                      {'5', '6'},
                                      {'4', '6'},
                                      {'7', '8', '9', '4'},
                                      {'7', '8', '9', '5'},
                                      {'7', '8', '9', '6'}], [0, 1, 2, 6, 7, 8], [{'1', '2', '3'}, {'1', '2', '3'}, {'1', '2', '3'}, {'7', '8', '9'}, {'7', '8', '9'}, {'7', '8', '9'}]))

    def _assertMsg(self, row, column, modification, possibilities):
        messageParts = [
            f"\nRow: {row}, Column: {column} \nModification: {modification} \nPossibilities:"]
        for curRow in possibilities:
            messageParts.append(f"{curRow}")
        return "\n".join(messageParts)

    def test_row(self):
        """ Tests that the single value is correctly detected in a row """
        MODIFIED_ROW = 2
        for modification in self.tests:
            self.basePossibilities[MODIFIED_ROW] = modification.startingValues
            reducedProbabilities = self.reducer.reduceByRow(
                self.basePossibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            for i in range(len(self.basePossibilities)):
                if i in modification.modifiedPositions:
                    self.assertSetEqual(
                        reducedProbabilities[MODIFIED_ROW][i], modification.modifiedValues[modification.modifiedPositions.index(i)], self._assertMsg(MODIFIED_ROW, i, modification, reducedProbabilities))
                else:
                    self.assertSetEqual(
                        reducedProbabilities[MODIFIED_ROW][i], self.basePossibilities[MODIFIED_ROW][i], self._assertMsg(MODIFIED_ROW, i, modification, reducedProbabilities))

    def test_column(self):
        """ Tests that the single value is correctly detected in a column """
        MODIFIED_COLUMN = 2
        for modification in self.tests:
            for i in range(len(self.basePossibilities)):
                self.basePossibilities[i][MODIFIED_COLUMN] = modification.startingValues[i]

            reducedProbabilities = self.reducer.reduceByColumn(
                self.basePossibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            for i in range(len(self.basePossibilities)):
                if i in modification.modifiedPositions:
                    self.assertSetEqual(
                        reducedProbabilities[i][MODIFIED_COLUMN], modification.modifiedValues[modification.modifiedPositions.index(i)], self._assertMsg(i, MODIFIED_COLUMN, modification, reducedProbabilities))
                else:
                    self.assertSetEqual(
                        reducedProbabilities[i][MODIFIED_COLUMN], self.basePossibilities[i][MODIFIED_COLUMN], self._assertMsg(i, MODIFIED_COLUMN, modification, reducedProbabilities))

    def test_square(self):
        """ Tests that the single value is correctly detected in a square """
        ROW_BASE = 3
        COLUMN_BASE = 3

        for modification in self.tests:

            modficationNumber = 0

            for i in range(3):
                for j in range(3):
                    row = ROW_BASE + i
                    column = COLUMN_BASE + j
                    self.basePossibilities[row][column] = modification.startingValues[modficationNumber]
                    modficationNumber += 1

            reducedProbabilities = self.reducer.reduceBySquare(
                self.basePossibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            # modficationNumber and checkNumber are used in the same way
            checkNumber = 0
            for i in range(3):
                for j in range(3):
                    row = ROW_BASE + i
                    column = COLUMN_BASE + j
                    if checkNumber in modification.modifiedPositions:
                        self.assertSetEqual(
                            reducedProbabilities[row][column], modification.modifiedValues[modification.modifiedPositions.index(checkNumber)], self._assertMsg(row, column, modification, reducedProbabilities))
                    else:
                        self.assertSetEqual(
                            reducedProbabilities[row][column], self.basePossibilities[row][column], self._assertMsg(row, column, modification, reducedProbabilities))
                    checkNumber += 1


if __name__ == '__main__':
    unittest.main()
