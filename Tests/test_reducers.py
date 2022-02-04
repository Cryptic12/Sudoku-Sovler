import unittest

# from Controller.Reducers.OnePositionReducer import OnePositionReducer
# from Controller.Reducers.ForcedPositionsReducer import ForcedPositionsReducer

from Controller.Rules.Conditions.Conditions import UniqueCondition
from Controller.Rules.Rules import RowRule, ColumnRule, SquareRule
from Controller.Reducers.Reducers import OnePositionReducer, ForcedPositionsReducer, ForcedPositionsInSquareReducer

from Tests.SudokuTest import SudokuTest

BOARD_SIZE = 9
SQUARE_SIZE = 3

CONDITIONS = [UniqueCondition()]

ROW_RULE = RowRule(BOARD_SIZE, CONDITIONS)
COLUMN_RULE = ColumnRule(BOARD_SIZE, CONDITIONS)
SQUARE_RULE = SquareRule(BOARD_SIZE, SQUARE_SIZE, CONDITIONS)


class TestOnePositionReducer(unittest.TestCase):

    def setUp(self):

        self.reducer = OnePositionReducer(BOARD_SIZE, SQUARE_SIZE, [
                                          ROW_RULE, COLUMN_RULE, SQUARE_RULE])
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
        self.tests.append(SudokuTest(starting_values=[{'1', '2'},
                                                      {'1', '2'},
                                                      {'3', '4'},
                                                      {'3', '4'},
                                                      {'5', '6'},
                                                      {'6', '7'},
                                                      {'6', '7'},
                                                      {'8', '9'},
                                                      {'8', '9'}], reductions={4: {'5'}}))

        # Check that multiple reductions are made
        self.tests.append(SudokuTest(starting_values=[{'1', '2', '3', '4', '5', '6', '7', '8'},
                                                      {'1', '2', '3', '4',
                                                          '5', '6', '7'},
                                                      {'1', '2', '3', '4',
                                                          '5', '6', '7'},
                                                      {'1', '2', '3', '4',
                                                          '5', '6', '7'},
                                                      {'1', '2', '3', '4',
                                                          '5', '6', '7'},
                                                      {'1', '2', '3', '4',
                                                          '5', '6', '7'},
                                                      {'1', '2', '3', '4',
                                                          '5', '6', '7'},
                                                      {'1', '2', '3', '4',
                                                          '5', '6', '7'},
                                                      {'1', '2', '3', '4', '5', '6', '7', '9'}], reductions={0: {'8'}, 8: {'9'}}))

        # Check that no changes are made when no reductions are possible
        self.tests.append(SudokuTest(starting_values=[{'1', '2'},
                                                      {'2', '3'},
                                                      {'3', '4'},
                                                      {'4', '5'},
                                                      {'5', '6'},
                                                      {'6', '7'},
                                                      {'7', '8'},
                                                      {'8', '9'},
                                                      {'9', '1'}], reductions={}))

        self.tests.append(SudokuTest(starting_values=[{'9'},
                                                      {'3'},
                                                      {'1', '4'},
                                                      {'5', '6'},
                                                      {'5', '6'},
                                                      {'1', '7'},
                                                      {'2'},
                                                      {'8'},
                                                      {'1', '4', '7'}], reductions={}))

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
            reductions = self.reducer.generic_reduce(
                self.base_possibilities, ROW_RULE.get_all_positions())

            self.assertEqual(len(reductions), len(modification.reductions))

            for reduction in reductions:
                position, change = reduction
                _, column = position
                self.assertIn(column, modification.reductions)
                self.assertSetEqual(change, modification.reductions[column])

    def test_column_mode(self):
        """ Tests that the single value is correctly detected in a column """
        MODIFIED_COLUMN = 2
        for modification in self.tests:
            for i in range(len(self.base_possibilities)):
                self.base_possibilities[i][MODIFIED_COLUMN] = modification.starting_values[i]

            reductions = self.reducer.generic_reduce(
                self.base_possibilities, COLUMN_RULE.get_all_positions())

            self.assertEqual(len(reductions), len(modification.reductions))

            for reduction in reductions:
                position, change = reduction
                row, _ = position
                self.assertIn(row, modification.reductions)
                self.assertSetEqual(change, modification.reductions[row])

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

            reductions = self.reducer.generic_reduce(
                self.base_possibilities, SQUARE_RULE.get_all_positions())

            self.assertEqual(len(reductions), len(modification.reductions))

            for reduction in reductions:
                position, change = reduction
                row, column = position
                index = (row % 3) * 3 + (column % 3)
                self.assertIn(index, modification.reductions)
                self.assertSetEqual(change, modification.reductions[index])


class TestForcedPositionsReducer(unittest.TestCase):

    def setUp(self):

        self.reducer = ForcedPositionsReducer(BOARD_SIZE, SQUARE_SIZE, [
            ROW_RULE, COLUMN_RULE, SQUARE_RULE])
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
        self.tests.append(SudokuTest(starting_values=[{'1'},
                                                      {'2'},
                                                      {'3'},
                                                      {'4'},
                                                      {'5'},
                                                      {'6'},
                                                      {'7'},
                                                      {'8'},
                                                      {'9'}],
                                     reductions={}))

        # Check that the values are correctly removed for a permutation of 2 values
        self.tests.append(SudokuTest(starting_values=[{'1'},
                                                      {'2'},
                                                      {'3', '4', '9'},
                                                      {'5', '6', '3'},
                                                      {'5', '6', '4'},
                                                      {'3', '4', '9'},
                                                      {'7'},
                                                      {'8'},
                                                      {'3', '4', '9'}],
                                     reductions={3: {'5', '6'}, 4: {'5', '6'}}))

        # Check that the values are correctly removed for a permutation of 3 values
        self.tests.append(SudokuTest(starting_values=[{'1', '2', '3', '7'},
                                                      {'1', '2', '3', '8'},
                                                      {'1', '2', '3', '9'},
                                                      {'4'},
                                                      {'5'},
                                                      {'6'},
                                                      {'7', '8'},
                                                      {'8', '9'},
                                                      {'7', '9'}],
                                     reductions={0: {'1', '2', '3'}, 1: {'1', '2', '3'}, 2: {'1', '2', '3'}}))

        # Check that multiple permutation replacements can be handled at once
        self.tests.append(SudokuTest(starting_values=[{'1', '2', '3', '4'},
                                                      {'1', '2', '3', '5'},
                                                      {'1', '2', '3', '6'},
                                                      {'4', '5'},
                                                      {'5', '6'},
                                                      {'4', '6'},
                                                      {'7', '8', '9', '4'},
                                                      {'7', '8', '9', '5'},
                                                      {'7', '8', '9', '6'}],
                                     reductions={0: {'1', '2', '3'}, 1: {'1', '2', '3'}, 2: {'1', '2', '3'}, 6: {'7', '8', '9'}, 7: {'7', '8', '9'}, 8: {'7', '8', '9'}}))

        # Current Test
        self.tests.append(SudokuTest(starting_values=[{'1', '2', '7', '8', '9'},
                                                      {'1', '2', '7', '8'},
                                                      {'3'},
                                                      {'5'},
                                                      {'6'},
                                                      {'2', '8'},
                                                      {'4'},
                                                      {'2', '8'},
                                                      {'7', '9'}],
                                     reductions={0: {'1', '7', '9'}, 1: {'1', '7'}}))

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
            reductions = self.reducer.generic_reduce(
                self.base_possibilities, ROW_RULE.get_all_positions())

            self.assertEqual(len(reductions), len(modification.reductions))

            for reduction in reductions:
                position, change = reduction
                _, column = position
                self.assertIn(column, modification.reductions)
                self.assertSetEqual(change, modification.reductions[column])

    def test_column(self):
        """ Tests that the single value is correctly detected in a column """
        MODIFIED_COLUMN = 2
        for modification in self.tests:
            for i in range(len(self.base_possibilities)):
                self.base_possibilities[i][MODIFIED_COLUMN] = modification.starting_values[i]

            reductions = self.reducer.generic_reduce(
                self.base_possibilities, COLUMN_RULE.get_all_positions())

            self.assertEqual(len(reductions), len(modification.reductions))

            for reduction in reductions:
                position, change = reduction
                row, _ = position
                self.assertIn(row, modification.reductions)
                self.assertSetEqual(change, modification.reductions[row])

    def test_square(self):
        """ Tests that the single value is correctly detected in a square """
        ROW_BASE = 3
        COLUMN_BASE = 3

        for modification in self.tests:

            modfication_number = 0

            for i in range(SQUARE_SIZE):
                for j in range(SQUARE_SIZE):
                    row = ROW_BASE + i
                    column = COLUMN_BASE + j
                    self.base_possibilities[row][column] = modification.starting_values[modfication_number]
                    modfication_number += 1

            reductions = self.reducer.generic_reduce(
                self.base_possibilities, SQUARE_RULE.get_all_positions())

            self.assertEqual(len(reductions), len(modification.reductions))

            for reduction in reductions:
                position, change = reduction
                row, column = position
                index = (row % 3) * 3 + (column % 3)
                self.assertIn(index, modification.reductions)
                self.assertSetEqual(change, modification.reductions[index])


class TestForcedPositionsInSquareReducer(unittest.TestCase):

    def setUp(self):

        self.reducer = ForcedPositionsInSquareReducer(
            SQUARE_RULE, [ROW_RULE, COLUMN_RULE])
        self.base_possibilities = [
            [{'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}],
            [{'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}],
            [{'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}],
            [{'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}],
            [{'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}],
            [{'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}],
            [{'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}],
            [{'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}],
            [{'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}, {'0'}]
        ]

        self.tests = []

        # A solved square should have no changes in values
        self.tests.append(SudokuTest(starting_values=[{'1'},
                                                      {'2'},
                                                      {'3'},
                                                      {'4'},
                                                      {'5'},
                                                      {'6'},
                                                      {'7'},
                                                      {'8'},
                                                      {'9'}], reductions={}))

        # If a value is found in the first group, it should be removed from all other groups
        self.tests.append(SudokuTest(starting_values=[{'1'},
                                                      {'1'},
                                                      {'1'},
                                                      {'1', '4'},
                                                      {'1', '5'},
                                                      {'1', '6'},
                                                      {'1', '7'},
                                                      {'1', '8'},
                                                      {'1', '9'}], reductions={3: {'4'}, 4: {'5'}, 5: {'6'}, 6: {'7'}, 7: {'8'}, 8: {'9'}}))

        # If the value also appears outside the given square, it shouldn't be removed from the other groups
        self.tests.append(SudokuTest(starting_values=[{'0'},
                                                      {'0'},
                                                      {'0'},
                                                      {'0'},
                                                      {'0'},
                                                      {'0'},
                                                      {'0'},
                                                      {'0'},
                                                      {'0'}], reductions={}))

        # If a value is only found in a group which is not the first, it should be removed from all other groups
        self.tests.append(SudokuTest(starting_values=[{'0'},
                                                      {'0'},
                                                      {'0'},
                                                      {'0', '1'},
                                                      {'0', '1'},
                                                      {'0', '1'},
                                                      {'0', '1', '2'},
                                                      {'0', '1', '2'},
                                                      {'0', '1', '2'}], reductions={3: {'0'}, 4: {'0'}, 5: {'0'}, 6: {'0', '2'}, 7: {'0', '2'}, 8: {'0', '2'}}))

    def _assert_msg(self, row, column, modification, possibilities):
        message_parts = [
            f"\nRow: {row}, Column: {column} \nModification: {modification} \nPossibilities:"]
        for curRow in possibilities:
            message_parts.append(f"{curRow}")
        return "\n".join(message_parts)

    def test_row(self):
        for modification in self.tests:
            current_value = 0
            positions_being_tested = []
            for row in range(SQUARE_SIZE):
                for column in range(SQUARE_SIZE):
                    self.base_possibilities[row][column] = modification.starting_values[current_value]
                    positions_being_tested.append((row, column))
                    current_value += 1

            reductions = self.reducer.generic_reduce(
                self.base_possibilities, ROW_RULE.get_all_positions())

            self.assertEqual(len(reductions), len(modification.reductions))

            for reduction in reductions:
                position, change = reduction
                row, column = position
                index = (row % 3) * 3 + (column % 3)
                self.assertIn(index, modification.reductions)
                self.assertSetEqual(change, modification.reductions[index])

    def test_column(self):
        for modification in self.tests:
            current_value = 0
            positions_being_tested = []
            for column in range(SQUARE_SIZE):
                for row in range(SQUARE_SIZE):
                    self.base_possibilities[row][column] = modification.starting_values[current_value]
                    positions_being_tested.append((row, column))
                    current_value += 1

            reductions = self.reducer.generic_reduce(
                self.base_possibilities, COLUMN_RULE.get_all_positions())

            self.assertEqual(len(reductions), len(modification.reductions))

            for reduction in reductions:
                position, change = reduction
                row, column = position
                index = (column % 3) * 3 + (row % 3)
                self.assertIn(index, modification.reductions)
                self.assertSetEqual(change, modification.reductions[index])


# The checks are the same across the tests. Should be able to extract the assertions into the below functions

def row_check():
    pass


def column_check():
    pass


def square_check():
    pass


if __name__ == '__main__':
    unittest.main()
