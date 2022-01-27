import unittest

from Controller.Rules.Conditions.Conditions import UniqueCondition
from Controller.Rules.Rules import RowRule, ColumnRule, SquareRule

BOARD_SIZE = 9
SQUARE_SIZE = 3

CONDITIONS = [UniqueCondition()]


class TestRowRule(unittest.TestCase):

    def setUp(self):
        self.reducer = RowRule(CONDITIONS)

    def test_get_positions(self):
        test_row = self.reducer.get_positions(0)
        expected_array = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                          (0, 5), (0, 6), (0, 7), (0, 8)]

        self.assertCountEqual(test_row, expected_array)

        test_row = self.reducer.get_positions(2)
        expected_array = [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                          (2, 5), (2, 6), (2, 7), (2, 8)]

        self.assertCountEqual(test_row, expected_array)

    def test_get_all_positions(self):
        rows = self.reducer.get_all_positions()
        self.assertEqual(len(rows), BOARD_SIZE)

        for row in rows:
            self.assertEqual(len(row), BOARD_SIZE)

    def test_get_affected_positions(self):
        position_being_checked = (0, 0)
        affected_positions = self.reducer.get_affected_positions(
            position_being_checked)
        expected_affected_positions = {
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)}

        self._get_affected_positions_check(
            position_being_checked, affected_positions, expected_affected_positions)

        position_being_checked = (5, 6)
        affected_positions = self.reducer.get_affected_positions(
            position_being_checked)
        expected_affected_positions = {
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 7), (5, 8)}

        self._get_affected_positions_check(
            position_being_checked, affected_positions, expected_affected_positions)

    def _get_affected_positions_check(self, position_being_checked, affected_positions, expected_affected_positions):
        self.assertNotIn(position_being_checked, affected_positions)
        self.assertEqual(len(affected_positions), BOARD_SIZE - 1)
        self.assertSetEqual(affected_positions, expected_affected_positions)


class TestColumnRule(unittest.TestCase):

    def setUp(self):
        self.reducer = ColumnRule(CONDITIONS)

    def test_get_positions(self):
        test_column = self.reducer.get_positions(0)
        expected_array = [(0, 0), (1, 0), (2, 0), (3, 0),
                          (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]

        self.assertCountEqual(test_column, expected_array)

        test_column = self.reducer.get_positions(2)
        expected_array = [(0, 2), (1, 2), (2, 2), (3, 2),
                          (4, 2), (5, 2), (6, 2), (7, 2), (8, 2)]

        self.assertCountEqual(test_column, expected_array)

    def test_get_all_positions(self):
        columns = self.reducer.get_all_positions()
        self.assertEqual(len(columns), BOARD_SIZE)

        for column in columns:
            self.assertEqual(len(column), BOARD_SIZE)

    def test_get_affected_positions(self):
        position_being_checked = (0, 0)
        affected_positions = self.reducer.get_affected_positions(
            position_being_checked)
        expected_affected_positions = {
            (1, 0), (2, 0), (3, 0),
            (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)}

        self._get_affected_positions_check(
            position_being_checked, affected_positions, expected_affected_positions)

        position_being_checked = (4, 4)
        affected_positions = self.reducer.get_affected_positions(
            position_being_checked)
        expected_affected_positions = {
            (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4), (8, 4)}

        self._get_affected_positions_check(
            position_being_checked, affected_positions, expected_affected_positions)

    def _get_affected_positions_check(self, position_being_checked, affected_positions, expected_affected_positions):
        self.assertNotIn(position_being_checked, affected_positions)
        self.assertEqual(len(affected_positions), BOARD_SIZE - 1)
        self.assertSetEqual(affected_positions, expected_affected_positions)


class TestSquareRule(unittest.TestCase):

    def setUp(self):
        self.reducer = SquareRule(SQUARE_SIZE, CONDITIONS)

    def test_get_positions(self):
        test_square = self.reducer.get_positions(0)
        expected_array = [(0, 0), (1, 0), (2, 0), (0, 1),
                          (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]

        self.assertCountEqual(test_square, expected_array)

        test_square = self.reducer.get_positions(4)
        expected_array = [(3, 3), (3, 4), (3, 5), (4, 3),
                          (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]

        self.assertCountEqual(test_square, expected_array)

        test_square = self.reducer.get_positions(8)
        expected_array = [(6, 6), (6, 7), (6, 8), (7, 6),
                          (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]

        self.assertCountEqual(test_square, expected_array)

    def test_get_all_positions(self):
        squares = self.reducer.get_all_positions()
        self.assertEqual(len(squares), BOARD_SIZE)

        for square in squares:
            self.assertEqual(len(square), BOARD_SIZE)

    def test_get_affected_positions(self):
        position_being_checked = (0, 0)
        affected_positions = self.reducer.get_affected_positions(
            position_being_checked)
        expected_affected_positions = {
            (1, 0), (2, 0), (0, 1),
            (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)}

        self._get_affected_positions_check(
            position_being_checked, affected_positions, expected_affected_positions)

        position_being_checked = (4, 4)
        affected_positions = self.reducer.get_affected_positions(
            position_being_checked)
        expected_affected_positions = {
            (3, 3), (3, 4), (3, 5), (4, 3),
            (4, 5), (5, 3), (5, 4), (5, 5)}

        self._get_affected_positions_check(
            position_being_checked, affected_positions, expected_affected_positions)

        position_being_checked = (7, 1)
        affected_positions = self.reducer.get_affected_positions(
            position_being_checked)
        expected_affected_positions = {
            (6, 0), (6, 1), (6, 2), (7, 0),
            (7, 2), (8, 0), (8, 1), (8, 2)}

        self._get_affected_positions_check(
            position_being_checked, affected_positions, expected_affected_positions)

    def _get_affected_positions_check(self, position_being_checked, affected_positions, expected_affected_positions):
        self.assertNotIn(position_being_checked, affected_positions)
        self.assertEqual(len(affected_positions), BOARD_SIZE - 1)
        self.assertSetEqual(affected_positions, expected_affected_positions)


if __name__ == '__main__':
    unittest.main()
