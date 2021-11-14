
class SudokuController:

    _sudoku_model = None
    _sudoku_rules = None
    _probability_reducer = None
    _solved = False

    def __init__(self, model, rules, reducer):

        self._sudoku_model = model
        self._sudoku_rules = rules
        self._probability_reducer = reducer

    def solve_sudoku(self):
        if self._solved:
            return

        self.generate_possibilities()
        self.reduce_possibilities()
        was_updated = self.update_board()

        if was_updated:
            self.solve_sudoku()

    def get_iterations(self):
        return self._iterations

    def is_solved(self):
        return self._solved

    def generate_possibilities(self):
        self._sudoku_model.set_possibilities(self._sudoku_rules.generate_possibilities(
            self._sudoku_model.get_board()))

    def reduce_possibilities(self):
        possibilities = self._sudoku_model.get_possibilities()
        self._sudoku_model.set_possibilities(
            self._probability_reducer.reduce_possibilities(possibilities))

    def update_board(self):
        board_modified = False
        board_size = self._sudoku_model.get_board_size()
        for i in range(board_size):
            for j in range(board_size):
                position = (i, j)
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


def main():
    pass


if __name__ == '__main__':
    main()
