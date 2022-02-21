import math
from multiprocessing.dummy import Array
from Other.Maths.Permutations import generate_permutation


class Reducer():

    def __init__(self, rules):
        self.rules = rules

    # Reduces the reductions by combinding reductions for the same positions and removing invalid (empty) reductions
    def reduce_reductions(self, reductions):
        reduced_reductions = dict()

        for reduction in reductions:
            position, possibilities = reduction

            if len(possibilities) == 0:
                continue

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

    # Returns a list of reductions made for each rule
    def reduce(self, possibilities):
        reductions = []

        for rule in self.rules:
            reductions.extend(self.generic_reduce(
                possibilities, rule.get_all_positions()))

        return self.reduce_reductions(reductions)

    # Identify values which only appear in a single positions possiblilites in a given group and reduce that positions possibilities to only that value

    def generic_reduce(self, possibilities, groups):

        reductions = []

        for group in groups:

            group_possibilities = self.get_group_possibilities(
                possibilities, group)
            single_values = self.identify_single_values(group_possibilities)

            if len(single_values) == 0:
                continue

            for position in group:

                row, column = position

                for value in single_values:

                    if len(possibilities[row][column]) <= 1:
                        continue

                    if value in possibilities[row][column]:
                        reductions.append((position, set(value)))

        return self.reduce_reductions(reductions)

    # Returns an array containing the possibilities for each position in the group
    def get_group_possibilities(self, possibilities, group):
        group_possibilities = []

        for position in group:
            row, column = position
            group_possibilities.append(
                possibilities[row][column])

        return group_possibilities

    # Returns values which only appear once in the possibilites

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


class ForcedPositionsInSquareReducer(Reducer):
    """ Checks if a value for a given group only belongs to possibilites for positions in the same square.
        If they are, we can remove that value as a possibility from all other positions within the square.
    """

    def __init__(self, square_rule, rules):
        super().__init__(rules)
        self.square_rule = square_rule

    # Returns a list of reductions made for each rule
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

                positions_containing_value = self.positions_containing_value(
                    possibilities, group, value)

                if len(positions_containing_value) == 0:
                    continue

                # Get the positions for a sqaure that one of the positions belong to
                square_positions = self.square_rule.get_affected_positions(
                    positions_containing_value[0])
                square_positions.add(positions_containing_value[0])

                # If all of the positions are in the same square, we can make reductions to the other positions in the square
                if self.all_positions_in_same_square(positions_containing_value, square_positions):
                    reductions.extend(self.identify_reductions(
                        possibilities, positions_containing_value, square_positions, value))

        return self.reduce_reductions(reductions)

    # Returns the positions which contain the value in their possibilities
    def positions_containing_value(self, possibilities, group, value):
        positions_containing_value = []
        for position in group:
            row, column = position
            if value in possibilities[row][column]:
                positions_containing_value.append(position)
        return positions_containing_value

    # Check if all positions containing the value are within the same square
    def all_positions_in_same_square(self, positions, square_positions):
        for position_containing_value in positions:
            if position_containing_value not in square_positions:
                return False

        return True

    # Identifies which positions inside of the square can have the value removed from it
    def identify_reductions(self, possibilities,  positions_containing_value, square_positions, value):
        reductions = []
        for position in square_positions:
            row, column = position

            if position in positions_containing_value:
                continue

            if value not in possibilities[row][column]:
                continue

            position_possibilities = possibilities[row][column].copy(
            )
            position_possibilities.remove(value)

            reductions.append((position, position_possibilities))

        return reductions


class ForcedPositionsReducer(Reducer):
    """ Identifies sets of positions in a given row/column/square where a subset of values are forced to be placed into """

    def __init__(self, board_size, square_size, rules):
        super().__init__(rules)
        self.board_size = board_size
        self.square_size = square_size

    # Returns a list of reductions made for each rule
    def reduce(self, possibilities):

        reductions = []

        for rule in self.rules:
            reductions.extend(self.generic_reduce(
                possibilities, rule.get_all_positions()))

        return self.reduce_reductions(reductions)

    def generic_reduce(self, possibilities, groups):
        reductions = []
        for group in groups:

            positions = self.unsolved_positions(possibilities, group)
            value_counts = self.calculate_value_counts(
                possibilities, positions)

            # No reductions can be made if these is only 1 value in the possibilites
            if len(value_counts) < 1:
                continue

            reductions.extend(self.do_permutations(
                possibilities, positions, value_counts))

        return self.reduce_reductions(reductions)

    # Reduce positions to those that have multiple possibilities
    def unsolved_positions(self, possibilities, group):
        positions = []
        for position in group:
            row, column = position

            if len(possibilities[row][column]) <= 1:
                continue

            positions.append(position)

        return positions

    # Counts the number of times each value appears in the possibilities of all positions
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

    # For the given group, check if any subset of positions only contain a subset of values equal to the number of positions being checked
    def do_permutations(self, possibilities, positions, value_counts):

        VALUE_COUNTS_MIN = min(value_counts.values())
        reductions = []

        # Check till 2 fewer than the total number of unsolved spaces
        for permutation_size in range(VALUE_COUNTS_MIN, len(positions) - 1):

            permutations = generate_permutation(positions, permutation_size)

            for permutation in permutations:

                # Positions that aren't in the permutation positions
                other_positions = set(
                    position for position in positions if position not in permutation)

                permutation_set, other_set = self.get_reduced_possibilities(
                    possibilities, permutation, other_positions)

                position_sizes = self.get_possibility_sizes(
                    possibilities, permutation)

                # Identify which values appear in the possibilities from the permutations positions and not in the other positions
                difference = permutation_set.difference(other_set)

                # If the number of positions in the permuation is equal to the number of possibilities only found in the permutation possibilities,
                # these positions must only contain these values and we can therefore remove all other possibilities
                if len(difference) == permutation_size:
                    reductions.extend(self.permutation_based_reductions(
                        possibilities, permutation, difference))
                elif len(position_sizes) == 1 and len(permutation_set) == permutation_size and next(iter(position_sizes)) == permutation_size:
                    reductions.extend(self.non_permutation_based_reductions(
                        possibilities, permutation_set, other_positions))

        return reductions

    # Returns two sets.
    # The first containing values found in the possibilities from positions that are part of the permutation
    # The second containing values found in the possibilities from positions that are not part of the permutation
    def get_reduced_possibilities(self, possibilities, permutation, other_positions):
        permutation_set = set()
        other_set = set()

        for i, position in enumerate(permutation):
            row, column = position
            if i > 0:
                permutation_set.intersection_update(
                    possibilities[row][column])
            else:
                permutation_set.update(possibilities[row][column])

        for position in other_positions:
            row, column = position
            other_set.update(possibilities[row][column])

        return(permutation_set, other_set)

    # Returns a set containing the the sizes of the possibilities for the given positions
    def get_possibility_sizes(self, possibilities, positions):
        position_sizes = set()
        for position in positions:
            row, column = position
            position_sizes.add(len(possibilities[row][column]))
        return position_sizes

    # Identifies reductions that can be made to the positions from the permutation
    def permutation_based_reductions(self, possibilities, permutation, difference):
        reductions = []
        for position in permutation:
            row, column = position
            if len(possibilities[row][column]) > len(possibilities[row][column].intersection(difference)) > 0:
                reductions.append(
                    (position, possibilities[row][column].intersection(difference)))
        return reductions

    # Identifies reductions that can be made to the positions that aren't in the permutation
    def non_permutation_based_reductions(self, possibilities, permutation_set, other_positions):
        reductions = []
        for position in other_positions:
            row, column = position
            if len(possibilities[row][column].difference(permutation_set)) < len(possibilities[row][column]):
                reductions.append(
                    (position, possibilities[row][column].difference(permutation_set)))
        return reductions


def main():
    pass


if __name__ == '__main__':
    main()
