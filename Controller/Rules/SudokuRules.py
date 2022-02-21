
class SudokuRules():

    _rules = []

    def __init__(self, rules):
        self._rules = rules

    # Check if all rules allow the value to be placed in the given position
    def check(self, solved_values, value, position):
        for rule in self._rules:
            if not rule.is_allowed(solved_values, value, position):
                return False
        return True

    # Generates the base possibilities based on the given rules
    def generate_possibilities(self, board):

        BOARD_SIZE = len(board)
        possibilities = []
        solved_positions = []

        for x in range(BOARD_SIZE):
            row = []
            for y in range(BOARD_SIZE):
                allowed_values = set()
                if board[x][y] != "":
                    allowed_values.add(board[x][y])
                else:
                    for value in range(1, BOARD_SIZE + 1):
                        value = str(value)
                        if self.check(board, value, (x, y)):
                            allowed_values.add(value)

                row.append(allowed_values)

                if len(allowed_values) == 1:
                    solved_positions.append(
                        ((x, y), next(iter(allowed_values))))

            possibilities.append(row)

        possibilities = self._reduce_by_solved(possibilities, solved_positions)

        return possibilities

    # Take the base possibilities and reduce based on any positions which only contained a single possibility
    def _reduce_by_solved(self, possibilities, solved_positions):

        new_solved_positions = []

        for solved_position in solved_positions:
            position, value = solved_position

            affected_positions = self.affected_positions(position)

            for affected_position in affected_positions:
                row, column = affected_position

                if len(possibilities[row][column]) <= 1:
                    continue

                if value in possibilities[row][column]:
                    possibilities[row][column].remove(value)

                if len(possibilities[row][column]) == 1:
                    new_solved_positions.append(((row, column), next(
                        iter(possibilities[row][column]))))

        if len(new_solved_positions) > 0:
            possibilities = self._reduce_by_solved(
                possibilities, new_solved_positions)

        return possibilities

    # Returns all positions which belong to the same subset from any of the rules as the given position (same row, column, square)
    def affected_positions(self, position):
        positions = set()
        for rule in self._rules:
            positions = positions.union(
                rule.get_affected_positions(position))
        return positions


def main():
    pass


if __name__ == '__main__':
    main()
