import unittest

from Controller.Reducers.OnePositionReducer import OnePositionReducer
from Controller.Reducers.ForcedPositionsReducer import ForcedPositionsReducer

from Test.SudokuTest import SudokuTest

BOARD_SIZE = 9
SQUARE_SIZE = 3


class TestOnePositionReducer(unittest.TestCase):

    def setUp(self):

        self.reducer = OnePositionReducer(BOARD_SIZE, SQUARE_SIZE)
        self.base_possibilities = [
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

    def _assert_msg(self, row, column, modification, possibilities):
        message_parts = [
            f"\nRow: {row}, Column: {column} \nModification: {modification} \nPossibilities:"]
        for cur_row in possibilities:
            message_parts.append(f"{cur_row}")
        return "\n".join(message_parts)

    def test_row_mode(self):
        """ Tests that the single value is correctly detected in a row """
        MODIFIED_ROW = 2
        for modification in self.tests:
            self.base_possibilities[MODIFIED_ROW] = modification.starting_values
            reduced_probabilities = self.reducer.reduce_by_row(
                self.base_possibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            for i in range(len(self.base_possibilities)):
                if i in modification.modified_positions:
                    self.assertSetEqual(
                        reduced_probabilities[MODIFIED_ROW][i], modification.modified_values[modification.modified_positions.index(i)], self._assert_msg(MODIFIED_ROW, i, modification, reduced_probabilities))
                else:
                    self.assertSetEqual(
                        reduced_probabilities[MODIFIED_ROW][i], self.base_possibilities[MODIFIED_ROW][i], self._assert_msg(MODIFIED_ROW, i, modification, reduced_probabilities))

    def test_column_mode(self):
        """ Tests that the single value is correctly detected in a column """
        MODIFIED_COLUMN = 2
        for modification in self.tests:
            for i in range(len(self.base_possibilities)):
                self.base_possibilities[i][MODIFIED_COLUMN] = modification.starting_values[i]

            reduced_probabilities = self.reducer.reduce_by_column(
                self.base_possibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            for i in range(len(self.base_possibilities)):
                if i in modification.modified_positions:
                    self.assertSetEqual(
                        reduced_probabilities[i][MODIFIED_COLUMN], modification.modified_values[modification.modified_positions.index(i)], self._assertMsg(i, MODIFIED_COLUMN, modification, reduced_probabilities))
                else:
                    self.assertSetEqual(
                        reduced_probabilities[i][MODIFIED_COLUMN], self.base_possibilities[i][MODIFIED_COLUMN], self._assert_msg(i, MODIFIED_COLUMN, modification, reduced_probabilities))

    def test_square_mode(self):
        """ Tests that the single value is correctly detected in a square """
        ROW_BASE = 3
        COLUMN_BASE = 3

        for modification in self.tests:

            modfication_number = 0

            for i in range(3):
                for j in range(3):
                    row = ROW_BASE + i
                    column = COLUMN_BASE + j
                    self.base_possibilities[row][column] = modification.starting_values[modfication_number]
                    modfication_number += 1

            reduced_probabilities = self.reducer.reduce_by_square(
                self.base_possibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            # modficationNumber and checkNumber are used in the same way
            check_number = 0
            for i in range(3):
                for j in range(3):
                    row = ROW_BASE + i
                    column = COLUMN_BASE + j
                    if check_number in modification.modified_positions:
                        self.assertSetEqual(
                            reduced_probabilities[row][column], modification.modified_values[modification.modified_positions.index(check_number)], self._assert_msg(row, column, modification, reduced_probabilities))
                    else:
                        self.assertSetEqual(
                            reduced_probabilities[row][column], self.base_possibilities[row][column], self._assert_msg(row, column, modification, reduced_probabilities))
                    check_number += 1


class TestForcedPositionsReducer(unittest.TestCase):

    def setUp(self):

        self.reducer = ForcedPositionsReducer(BOARD_SIZE, SQUARE_SIZE)
        self.base_possibilities = [
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

    def _assert_msg(self, row, column, modification, possibilities):
        message_parts = [
            f"\nRow: {row}, Column: {column} \nModification: {modification} \nPossibilities:"]
        for curRow in possibilities:
            message_parts.append(f"{curRow}")
        return "\n".join(message_parts)

    def test_row(self):
        """ Tests that the single value is correctly detected in a row """
        MODIFIED_ROW = 2
        for modification in self.tests:
            self.base_possibilities[MODIFIED_ROW] = modification.starting_values
            reduced_probabilities = self.reducer.reduce_by_row(
                self.base_possibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            for i in range(len(self.base_possibilities)):
                if i in modification.modified_positions:
                    self.assertSetEqual(
                        reduced_probabilities[MODIFIED_ROW][i], modification.modified_values[modification.modified_positions.index(i)], self._assert_msg(MODIFIED_ROW, i, modification, reduced_probabilities))
                else:
                    self.assertSetEqual(
                        reduced_probabilities[MODIFIED_ROW][i], self.base_possibilities[MODIFIED_ROW][i], self._assert_msg(MODIFIED_ROW, i, modification, reduced_probabilities))

    def test_column(self):
        """ Tests that the single value is correctly detected in a column """
        MODIFIED_COLUMN = 2
        for modification in self.tests:
            for i in range(len(self.base_possibilities)):
                self.base_possibilities[i][MODIFIED_COLUMN] = modification.starting_values[i]

            reduced_probabilities = self.reducer.reduce_by_column(
                self.base_possibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            for i in range(len(self.base_possibilities)):
                if i in modification.modified_positions:
                    self.assertSetEqual(
                        reduced_probabilities[i][MODIFIED_COLUMN], modification.modified_values[modification.modified_positions.index(i)], self._assert_msg(i, MODIFIED_COLUMN, modification, reduced_probabilities))
                else:
                    self.assertSetEqual(
                        reduced_probabilities[i][MODIFIED_COLUMN], self.base_possibilities[i][MODIFIED_COLUMN], self._assert_msg(i, MODIFIED_COLUMN, modification, reduced_probabilities))

    def test_square(self):
        """ Tests that the single value is correctly detected in a square """
        ROW_BASE = 3
        COLUMN_BASE = 3

        for modification in self.tests:

            modfication_number = 0

            for i in range(3):
                for j in range(3):
                    row = ROW_BASE + i
                    column = COLUMN_BASE + j
                    self.base_possibilities[row][column] = modification.starting_values[modfication_number]
                    modfication_number += 1

            reduced_probabilities = self.reducer.reduce_by_square(
                self.base_possibilities)

            # Check that all the expected reductions and only the expected reductions have been made
            # modficationNumber and checkNumber are used in the same way
            check_number = 0
            for i in range(3):
                for j in range(3):
                    row = ROW_BASE + i
                    column = COLUMN_BASE + j
                    if check_number in modification.modified_positions:
                        self.assertSetEqual(
                            reduced_probabilities[row][column], modification.modified_values[modification.modified_positions.index(check_number)], self._assert_msg(row, column, modification, reduced_probabilities))
                    else:
                        self.assertSetEqual(
                            reduced_probabilities[row][column], self.base_possibilities[row][column], self._assert_msg(row, column, modification, reduced_probabilities))
                    check_number += 1


if __name__ == '__main__':
    unittest.main()
