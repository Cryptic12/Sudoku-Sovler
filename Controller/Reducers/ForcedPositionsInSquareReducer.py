from Controller.Rules.Rules import SquareRule


class ForcedPositionsInSquareReducer():
    """ Checks if all of the positions that contain a given value as a possibility are within the same square.
        If they are, we can remove that value as a possibility from all other positions within the square.
    """

    def __init__(self, square_rule):
        self._square_rule = square_rule

    def reduce(self, possibilities):
        possibilities = self.reduce_by_row(possibilities)
        possibilities = self.reduce_by_column(possibilities)
        return possibilities

    def reduce_by_row(self, possibilities):
        POSSIBILITIES_SIZE = len(possibilities)
        possible_values = []

        for value in range(0, POSSIBILITIES_SIZE):
            possible_values.append(str(value + 1))

        for value in possible_values:
            for row in range(POSSIBILITIES_SIZE):
                positions_containing_value = []
                for column in range(POSSIBILITIES_SIZE):
                    if value in possibilities[row][column]:
                        positions_containing_value.append((row, column))

                #  Check if all positions containing the value are within the same square
                square_positions = set()
                for position_containing_value in positions_containing_value:
                    if len(square_positions) == 0:
                        square_positions = self._square_rule.get_affected_positions(
                            position_containing_value)
                    else:
                        square_positions = square_positions.union(
                            self._square_rule.get_affected_positions(position_containing_value))

                if len(square_positions) == POSSIBILITIES_SIZE:
                    for position in square_positions:
                        square_row, square_column = position
                        if square_row != row and value in possibilities[square_row][square_column]:
                            position_possibilities = possibilities[square_row][square_column].copy(
                            )
                            position_possibilities.remove(value)
                            possibilities[square_row][square_column] = position_possibilities

        return possibilities

    def reduce_by_column(self, possibilities):

        POSSIBILITIES_SIZE = len(possibilities)
        possible_values = []

        for value in range(0, POSSIBILITIES_SIZE):
            possible_values.append(str(value + 1))

        for value in possible_values:
            for column in range(POSSIBILITIES_SIZE):
                positions_containing_value = []
                for row in range(POSSIBILITIES_SIZE):
                    if value in possibilities[row][column]:
                        positions_containing_value.append((row, column))

                #  Check if all positions containing the value are within the same square
                square_positions = set()
                for position_containing_value in positions_containing_value:
                    if len(square_positions) == 0:
                        square_positions = self._square_rule.get_affected_positions(
                            position_containing_value)
                    else:
                        square_positions = square_positions.union(
                            self._square_rule.get_affected_positions(position_containing_value))

                if len(square_positions) == POSSIBILITIES_SIZE:
                    for position in square_positions:
                        square_row, square_column = position
                        if square_column != column and value in possibilities[square_row][square_column]:
                            position_possibilities = possibilities[square_row][square_column].copy(
                            )
                            position_possibilities.remove(value)
                            possibilities[square_row][square_column] = position_possibilities

        return possibilities
