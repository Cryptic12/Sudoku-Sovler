
import math


class OnePositionReducer:
    """ Reduces posibilities by identifying positions in a given row/column/square that is the only position in the given row/column/square where it can be placed """

    def __init__(self, board_size, square_size, rules):
        self._board_size = board_size
        self._square_size = square_size
        self._rules = rules

    def identify_single_values(self, possibilities):

        value_counts = dict()
        for possibility in possibilities:
            for value in possibility:
                count = value_counts.get(value)
                if count == None:
                    value_counts[value] = 1
                else:
                    value_counts[value] = count + 1

        single_values = []

        for key in value_counts:
            if value_counts[key] == 1:
                single_values.append(key)

        return single_values

    def reduce(self, possibilities):
        possibilities = self.reduce_by_row(possibilities)
        possibilities = self.reduce_by_column(possibilities)
        possibilities = self.reduce_by_square(possibilities)

        return possibilities

    def reduce_by_row(self, possibilities):
        changes = []
        for row in range(self._board_size):
            cur_row = possibilities[row].copy()
            single_values = self.identify_single_values(cur_row)

            if len(single_values) == 0:
                continue

            for column in range(self._board_size):
                for value in single_values:
                    if value in possibilities[row][column] and len(possibilities[row][column]) > 1:
                        possibilities[row][column] = set(value)
                        change = ((row, column), value)
                        changes.append(change)

        if len(changes) > 0:
            # print("Row", changes)
            possibilities = self._update_affected_positions(
                possibilities, changes)

        return possibilities

    def reduce_by_column(self, possibilities):
        changes = []
        for column in range(self._board_size):
            cur_column = []
            for row in range(self._board_size):
                cur_column.append(possibilities[row][column])

            single_values = self.identify_single_values(cur_column)

            if len(single_values) == 0:
                continue

            for row in range(self._board_size):
                for value in single_values:
                    if value in possibilities[row][column] and len(possibilities[row][column]) > 1:
                        possibilities[row][column] = set(value)
                        change = ((row, column), value)
                        changes.append(change)

        if len(changes) > 0:
            # print("Column", changes)
            possibilities = self._update_affected_positions(
                possibilities, changes)

        return possibilities

    def reduce_by_square(self, possibilities):

        SQUARE_COUNT = int(self._board_size / self._square_size) ** 2
        changes = []

        for square in range(0, SQUARE_COUNT):

            ROW_BASE = (square % self._square_size) * self._square_size
            COLUMN_BASE = math.floor(
                square / self._square_size) * self._square_size

            square_possibilities = []
            for row in range(self._square_size):
                cur_row = ROW_BASE + row
                for column in range(self._square_size):
                    cur_column = COLUMN_BASE + column
                    square_possibilities.append(
                        possibilities[cur_row][cur_column])

            single_values = self.identify_single_values(square_possibilities)

            # TODO the below code is roughly duplicated throughout the 3 functions. Should find a way to remove
            if len(single_values) == 0:
                continue

            for row in range(0, self._square_size):
                cur_row = ROW_BASE + row
                for column in range(0, self._square_size):
                    cur_column = COLUMN_BASE + column
                    for value in single_values:
                        if value in possibilities[cur_row][cur_column] and len(possibilities[cur_row][cur_column]) > 1:
                            possibilities[cur_row][cur_column] = set(value)
                            change = ((cur_row, cur_column), value)
                            changes.append(change)

        if len(changes) > 0:
            # print("Square", changes)
            possibilities = self._update_affected_positions(
                possibilities, changes)

        return possibilities

    def _update_affected_positions(self, possibilities, changes):

        new_changes = []

        for change in changes:
            position, value = change
            affected_positions = set()

            for rule in self._rules:
                affected_positions = affected_positions.union(
                    rule.get_affected_positions(position))

            for affect_position in affected_positions:
                row, column = affect_position

                if value in possibilities[row][column] and len(possibilities[row][column]) > 1:
                    cur_possibilities = possibilities[row][column].copy()
                    cur_possibilities.remove(
                        value)
                    possibilities[row][column] = cur_possibilities

                    if len(cur_possibilities) == 1:
                        new_changes.append(((row, column), next(
                            iter(possibilities[row][column]))))

        if len(new_changes) > 0:
            # print(f"Extras: {new_changes} for {changes}")
            for row in possibilities:
                print(row)
            possibilities = self._update_affected_positions(
                possibilities, new_changes)

        return possibilities
