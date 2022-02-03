import math


class Reducer():

    def __init__(self, rules):
        self.rules = rules

    def reduce_reductions(self, reductions):
        reduced_reductions = dict()

        for reduction in reductions:
            position, possibilities = reduction
            # row, column = position

            if len(possibilities) > 0:
                if position in reduced_reductions:
                    reduced_reductions[position] = reduced_reductions[position].intersection(
                        possibilities)
                else:
                    reduced_reductions[position] = possibilities

        to_return = []
        for position in reduced_reductions:
            to_return.append((position, reduced_reductions[position]))

        return to_return


class OnePositionReducer(Reducer):
    """ Reduces posibilities by identifying positions in a given row/column/square that is the only position in the given row/column/square where it can be placed """

    def __init__(self, board_size, square_size, rules):
        super().__init__(rules)
        self.board_size = board_size
        self.square_size = square_size

    def identify_single_values(self, possibilities):

        value_counts = dict()
        for possibility in possibilities:
            # TODO Might be a reduce like method to simplfy this logic
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
        reductions = []

        for rule in self.rules:
            reductions.extend(self.generic_reduce(
                possibilities, rule.get_all_positions()))

        return self.reduce_reductions(reductions)

    def generic_reduce(self, possibilities, groups):

        reductions = []

        for group in groups:

            group_possibilities = []

            for position in group:
                row, column = position
                group_possibilities.append(
                    possibilities[row][column])

            single_values = self.identify_single_values(group_possibilities)

            if len(single_values) == 0:
                continue

            for position in group:
                row, column = position
                for value in single_values:
                    if value in possibilities[row][column] and len(possibilities[row][column]) > 1:
                        reductions.append((position, set(value)))

        return self.reduce_reductions(reductions)


class ForcedPositionsInSquareReducer(Reducer):
    """ Checks if all of the positions that contain a given value as a possibility are within the same square.
        If they are, we can remove that value as a possibility from all other positions within the square.
    """

    def __init__(self, square_rule, rules):
        super().__init__(rules)
        self.square_rule = square_rule

    def reduce(self, possibilities):
        reductions = []

        for rule in self.rules:

            reductions.extend(self.generic_reduce(
                possibilities, rule.get_all_positions()))

        return self.reduce_reductions(reductions)

    def generic_reduce(self, possibilities, groups):

        POSSIBILITIES_SIZE = len(possibilities)
        possible_values = []

        for value in range(0, POSSIBILITIES_SIZE):
            possible_values.append(str(value + 1))

        reductions = []

        for group in groups:

            for value in possible_values:
                positions_containing_value = []
                for position in group:
                    row, column = position

                    if value in possibilities[row][column]:
                        positions_containing_value.append(position)

                if len(positions_containing_value) == 0:
                    continue

                #  Check if all positions containing the value are within the same square
                square_positions = self.square_rule.get_affected_positions(
                    positions_containing_value.pop())
                all_positions_in_square = True
                for position_containing_value in positions_containing_value:
                    if position_containing_value not in square_positions:
                        all_positions_in_square = False

                if all_positions_in_square:
                    for position in square_positions:
                        row, column = position
                        if position in positions_containing_value or value not in possibilities[row][column]:
                            continue

                        # TODO confirm whether the set needs to be copied before the value is removed
                        position_possibilities = possibilities[row][column].copy(
                        )
                        position_possibilities.remove(value)

                        reductions.append((position, position_possibilities))

        return self.reduce_reductions(reductions)


class ForcedPositionsReducer(Reducer):
    """ Identifies sets of positions in a given row/column/square where a subset of values are forced to be placed into """

    def __init__(self, board_size, square_size, rules):
        super().__init__(rules)
        self.board_size = board_size
        self.square_size = square_size

    def reduce(self, possibilities):

        reductions = []

        for rule in self.rules:
            reductions.extend(self.generic_reduce(
                possibilities, rule.get_all_positions()))

        return self.reduce_reductions(reductions)

    def generic_reduce(self, possibilities, groups):
        reductions = []
        for group in groups:

            # For each position, count the number of times each value appears
            positions = []
            for position in group:
                row, column = position

                if len(possibilities[row][column]) <= 1:
                    continue

                positions.append(position)

            reductions.extend(self.reduce_positions_outer(
                possibilities, positions))

        return self.reduce_reductions(reductions)

    def reduce_positions_outer(self, possibilities, positions):
        value_counts = self.calculate_value_counts(possibilities, positions)

        if len(value_counts) < 1:
            return []

        return self.do_permutations(possibilities, positions, value_counts)

    def calculate_value_counts(self, possibilities, positions):
        value_counts = {}

        for position in positions:
            row, column = position
            possibility = possibilities[row][column]
            for value in possibility:
                if value in value_counts:
                    value_counts[value] = value_counts.get(value) + 1
                else:
                    value_counts[value] = 1

        return value_counts

    def do_permutations(self, possibilities, positions, value_counts):

        VALUE_COUNTS_MIN = min(value_counts.values())
        reductions = []

        # Check till 2 fewer than the total number of unsolved spaces
        for permutation_size in range(VALUE_COUNTS_MIN, len(positions) - 1):

            permutations = permutation_maker(positions, permutation_size)

            for permutation in permutations:
                permutation_set = set()
                position_sizes = set()
                other_set = set()

                for i, position in enumerate(permutation):
                    row, column = position
                    if i > 0:
                        permutation_set.intersection_update(
                            possibilities[row][column])
                    else:
                        permutation_set.update(possibilities[row][column])

                    position_sizes.add(len(possibilities[row][column]))

                other_positions = set(
                    position for position in positions if position not in permutation)

                for position in other_positions:
                    row, column = position
                    other_set.update(possibilities[row][column])

                # Identify which values appear in the possibilities from the permutations positions and not in the other positions
                difference = permutation_set.difference(other_set)

                # If the number of positions in the permuation is equal to the number of possibilities only found in the permutation possibilities,
                # these positions must only contain these values and we can therefore remove all other possibilities
                if len(difference) == permutation_size:
                    for position in permutation:
                        row, column = position
                        if len(possibilities[row][column]) > len(possibilities[row][column].intersection(difference)) > 0:
                            reductions.append(
                                (position, possibilities[row][column].intersection(difference)))
                elif len(position_sizes) == 1 and len(permutation_set) == permutation_size and next(iter(position_sizes)) == permutation_size:
                    for position in other_positions:
                        row, column = position
                        if len(possibilities[row][column].difference(permutation_set)) < len(possibilities[row][column]):
                            reductions.append(
                                (position, possibilities[row][column].difference(permutation_set)))

        return reductions


def permutation_maker(arr, cnt, result=[]):
    if (cnt == 0):
        return [result]

    to_return = []

    for i, value in enumerate(arr):
        to_return.extend(permutation_maker(
            arr[i + 1:], cnt - 1, [*result, value]))

    return to_return


def main():
    pass


if __name__ == '__main__':
    main()
