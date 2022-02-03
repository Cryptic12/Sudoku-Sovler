
from contextlib import redirect_stderr
from operator import truediv

from Tests.test_reducers import BOARD_SIZE


class SudokuController:

    _sudoku_model = None
    _sudoku_rules = None
    _probability_reducer = None
    _solved = False
    _solvable = True
    _iterations = 0

    def __init__(self, model, loader, rules, reducer):

        self._sudoku_model = model
        self._sudoku_loader = loader
        self._sudoku_rules = rules
        self._probability_reducer = reducer

    def solve_sudoku(self):
        if self._solved or not self._solvable:
            return

        BOARD_SIZE = self._sudoku_model.get_board_size()
        target_possibilities_total = BOARD_SIZE * BOARD_SIZE

        self.generate_possibilities()
        prev_possibilites_total = self.count_possibilities()

        while self._solvable and not self._solved:
            self._iterations += 1

            reductions = self.get_reductions()
            positions_solved = self.reduce_possibilities(reductions)
            self.update_board()

            if positions_solved > 0:
                self.generate_possibilities()
                continue

            possibilites_total = self.count_possibilities()

            if possibilites_total == target_possibilities_total:
                self._solved = True

            if possibilites_total == prev_possibilites_total:
                self._solvable = False

            if possibilites_total < prev_possibilites_total:
                prev_possibilites_total = possibilites_total

    def get_iterations(self):
        return self._iterations

    def is_solved(self):
        return self._solved

    def generate_possibilities(self):
        possibilities = self._sudoku_rules.generate_possibilities(
            self._sudoku_model.get_board())
        self._sudoku_model.set_possibilities(possibilities)

    def get_reductions(self):
        return self._probability_reducer.reduce_possibilities(
            self._sudoku_model.get_possibilities())

    def reduce_possibilities(self, reductions):

        positions_solved = 0

        for reduction in reductions:
            position, reduced_possibilities = reduction
            current_possibilities = self._sudoku_model.get_position_possibilities(
                position)
            new_possibilities = current_possibilities.intersection(
                reduced_possibilities)
            self._sudoku_model.set_position_possibilities(position,
                                                          new_possibilities)

            if len(current_possibilities) > 1 and len(new_possibilities) == 1:
                positions_solved += 1

        return positions_solved

    def update_board(self):
        board_modified = False
        BOARD_SIZE = self._sudoku_model.get_board_size()

        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                position = (row, column)

                if self._sudoku_model.get_value(position) != "":
                    continue

                probabilites = set(
                    self._sudoku_model.get_position_possibilities(position))

                if len(probabilites) > 1:
                    continue

                for value in probabilites:
                    self._sudoku_model.set_value(position, value)
                    board_modified = True

        return board_modified

    def count_possibilities(self):
        total = 0
        BOARD_SIZE = self._sudoku_model.get_board_size()

        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                position = (row, column)
                total += len(self._sudoku_model.get_position_possibilities(position))

        return total

    def reset_board(self):
        self._solved = False
        self._solvable = True
        self._iterations = 0
        self._sudoku_model.load_board(self._sudoku_loader.get_sudoku_board())


def main():
    pass


if __name__ == '__main__':
    main()
