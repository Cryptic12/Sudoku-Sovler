import unittest
import math

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


def make_position_key(row, column):
    return f"{row}_{column}"


def modifiy_possibilities_by_row(possibilities, modification, row):
    possibilities[row] = modification.starting_values
    return possibilities


def modifiy_possibilities_by_column(possibilities, modification, column):
    for i in range(len(possibilities)):
        possibilities[i][column] = modification.starting_values[i]
    return possibilities


def modifiy_possibilities_by_square(possibilities, modification, square, by_row=True):
    ROW_BASE, COLUMN_BASE = SQUARE_RULE.get_base_values(square)
    modfication_number = 0

    for i in range(SQUARE_SIZE):
        for j in range(SQUARE_SIZE):
            row = ROW_BASE + i if by_row else ROW_BASE + j
            column = COLUMN_BASE + j if by_row else COLUMN_BASE + i
            possibilities[row][column] = modification.starting_values[modfication_number]
            modfication_number += 1

    return possibilities


def make_modification_map_row(reductions, row):
    expected_reductions = dict()

    for column in reductions:
        position_key = make_position_key(row, column)
        expected_reductions[position_key] = reductions[column]

    return expected_reductions


def make_modification_map_column(reductions, column):
    expected_reductions = dict()

    for row in reductions:
        position_key = make_position_key(row, column)
        expected_reductions[position_key] = reductions[row]

    return expected_reductions


def make_modification_map_square(reductions, square, by_row=True):
    ROW_BASE, COLUMN_BASE = SQUARE_RULE.get_base_values(square)

    expected_reductions = dict()

    for i in reductions:
        modified_row = ROW_BASE + \
            math.floor(i / SQUARE_SIZE) if by_row else ROW_BASE + \
            (i % SQUARE_SIZE)
        modified_column = COLUMN_BASE + \
            (i % SQUARE_SIZE) if by_row else COLUMN_BASE + \
            math.floor(i / SQUARE_SIZE)
        position_key = make_position_key(modified_row, modified_column)
        expected_reductions[position_key] = reductions[i]

    return expected_reductions


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

    def _generic_test(self, rule, modification, expected_reductions):
        reductions = self.reducer.generic_reduce(
            self.base_possibilities, rule.get_all_positions())

        self.assertEqual(len(reductions), len(modification.reductions))

        for reduction in reductions:
            position, change = reduction
            row, column = position
            position_key = make_position_key(row, column)

            self.assertIn(position_key, expected_reductions)
            self.assertSetEqual(change, expected_reductions[position_key])

    def test_row_mode(self):
        """ Tests that the single value is correctly detected in a row """
        MODIFIED_ROW = 2
        for modification in self.tests:
            self.base_possibilities = modifiy_possibilities_by_row(
                self.base_possibilities, modification, MODIFIED_ROW)

            expected_reductions = make_modification_map_row(
                modification.reductions, MODIFIED_ROW)

            self._generic_test(ROW_RULE, modification, expected_reductions)

    def test_column_mode(self):
        """ Tests that the single value is correctly detected in a column """
        MODIFIED_COLUMN = 2
        for modification in self.tests:
            self.base_possibilities = modifiy_possibilities_by_column(
                self.base_possibilities, modification, MODIFIED_COLUMN)

            expected_reductions = make_modification_map_column(
                modification.reductions, MODIFIED_COLUMN)

            self._generic_test(COLUMN_RULE, modification, expected_reductions)

    def test_square_mode(self):
        """ Tests that the single value is correctly detected in a square """
        MODIFIED_SQUARE = 4

        for modification in self.tests:

            self.base_possibilities = modifiy_possibilities_by_square(
                self.base_possibilities, modification, MODIFIED_SQUARE)

            expected_reductions = make_modification_map_square(
                modification.reductions, MODIFIED_SQUARE)

            self._generic_test(SQUARE_RULE, modification, expected_reductions)


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

    def _generic_test(self, rule, modification, expected_reductions):
        reductions = self.reducer.generic_reduce(
            self.base_possibilities, rule.get_all_positions())

        self.assertEqual(len(reductions), len(modification.reductions))

        for reduction in reductions:
            position, change = reduction
            row, column = position
            position_key = make_position_key(row, column)

            self.assertIn(position_key, expected_reductions)
            self.assertSetEqual(change, expected_reductions[position_key])

    def test_row_rule(self):
        """ Tests that the single value is correctly detected in a row """
        MODIFIED_ROW = 2
        for modification in self.tests:
            self.base_possibilities = modifiy_possibilities_by_row(
                self.base_possibilities, modification, MODIFIED_ROW)

            expected_reductions = make_modification_map_row(
                modification.reductions, MODIFIED_ROW)

            self._generic_test(ROW_RULE, modification, expected_reductions)

    def test_column_rule(self):
        """ Tests that the single value is correctly detected in a column """
        MODIFIED_COLUMN = 2
        for modification in self.tests:
            self.base_possibilities = modifiy_possibilities_by_column(
                self.base_possibilities, modification, MODIFIED_COLUMN)

            expected_reductions = make_modification_map_column(
                modification.reductions, MODIFIED_COLUMN)

            self._generic_test(COLUMN_RULE, modification, expected_reductions)

    def test_square_rule(self):
        """ Tests that the single value is correctly detected in a square """
        MODIFIED_SQUARE = 4

        for modification in self.tests:

            self.base_possibilities = modifiy_possibilities_by_square(
                self.base_possibilities, modification, MODIFIED_SQUARE)

            expected_reductions = make_modification_map_square(
                modification.reductions, MODIFIED_SQUARE)

            self._generic_test(SQUARE_RULE, modification, expected_reductions)


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

    def _generic_test(self, rule, modification, expected_reductions):
        reductions = self.reducer.generic_reduce(
            self.base_possibilities, rule.get_all_positions())

        self.assertEqual(len(reductions), len(modification.reductions))

        for reduction in reductions:
            position, change = reduction
            row, column = position
            position_key = make_position_key(row, column)

            self.assertIn(position_key, expected_reductions)
            self.assertSetEqual(change, expected_reductions[position_key])

    def test_row_rule(self):
        MODIFIED_SQUARE = 0
        for modification in self.tests:
            self.base_possibilities = modifiy_possibilities_by_square(
                self.base_possibilities, modification, MODIFIED_SQUARE)

            expected_reductions = make_modification_map_square(
                modification.reductions, MODIFIED_SQUARE)

            self._generic_test(ROW_RULE, modification, expected_reductions)

    def test_column_rule(self):
        MODIFIED_SQUARE = 0
        for modification in self.tests:
            self.base_possibilities = modifiy_possibilities_by_square(
                self.base_possibilities, modification, MODIFIED_SQUARE, False)

            expected_reductions = make_modification_map_square(
                modification.reductions, MODIFIED_SQUARE, False)

            self._generic_test(COLUMN_RULE, modification, expected_reductions)


if __name__ == '__main__':
    unittest.main()
