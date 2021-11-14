import math


class ForcedPositionsReducer():
    """ Identifies sets of positions in a given row/column/square where a subset of values are forced to be placed into """

    def __init__(self, board_size, square_size):
        self.board_size = board_size
        self.square_size = square_size

    def reduce(self, possibilities):
        possibilities = self.reduce_by_row(possibilities)
        possibilities = self.reduce_by_column(possibilities)
        return self.reduce_by_square(possibilities)

    def reduce_by_row(self, possibilities):
        for row in range(self.board_size):

            # For each position, count the number of times each value appears
            positions = []
            for column in range(self.board_size):

                if len(possibilities[row][column]) <= 1:
                    continue

                positions.append((row, column))

            possibilities = reduce_positions_outer(possibilities, positions)

        return possibilities

    def reduce_by_column(self, possibilities):
        for column in range(self.board_size):

            # For each position, count the number of times each value appears
            positions = []
            for row in range(self.board_size):

                if len(possibilities[row][column]) <= 1:
                    continue

                positions.append((row, column))

            # print(f"Column: {column}")
            possibilities = reduce_positions_outer(possibilities, positions)

        return possibilities

    def reduce_by_square(self, possibilities):
        SQUARE_SIZE = self.square_size
        SQUARE_COUNT = int(self.board_size / SQUARE_SIZE) ** 2

        for square in range(0, SQUARE_COUNT):

            ROW_BASE = (square % SQUARE_SIZE) * SQUARE_SIZE
            COLUMN_BASE = math.floor(square / SQUARE_SIZE) * SQUARE_SIZE

            # For each position, count the number of times each value appears
            positions = []
            for x in range(0, SQUARE_SIZE):
                cur_row = ROW_BASE + x
                for y in range(0, SQUARE_SIZE):
                    cur_column = COLUMN_BASE + y

                    if len(possibilities[cur_row][cur_column]) <= 1:
                        continue

                    positions.append((cur_row, cur_column))

            # print(f"Square: {square}")
            possibilities = reduce_positions_outer(possibilities, positions)

        return possibilities


def reduce_positions_outer(possibilities, positions):
    value_counts = calculate_value_counts(possibilities, positions)

    if len(value_counts) < 1:
        return possibilities

    return do_permutations(possibilities, positions, value_counts)


def calculate_value_counts(possibilities, positions):
    value_counts = {}

    for position in positions:
        row, column = position
        possibility = possibilities[row][column]
        for value in possibility:
            count = value_counts.get(value)
            if count == None:
                value_counts[value] = 1
            else:
                value_counts[value] = count + 1

    return value_counts


def do_permutations(possibilities, positions, value_counts):

    VALUE_COUNTS_MIN = min(value_counts.values())

    # Check till 2 fewer than the total number of unsolved spaces
    for i in range(VALUE_COUNTS_MIN, len(positions) - 1):
        permutations = permutation_maker(positions, i)

        for permutation in permutations:
            group1 = set()
            group2 = set()
            for position in positions:
                x, y = position
                if position in permutation:
                    # Values that are in all of the positions
                    if group1:
                        group1 = group1.intersection(
                            possibilities[x][y])
                    else:
                        group1 = group1.union(
                            possibilities[x][y])
                else:
                    # Values found in any of the other positions
                    group2 = group2.union(
                        possibilities[x][y])

            difference = group1.difference(group2)
            if len(difference) == i:
                # print(
                #     f"~~~ {i} ~~~ \n possibilities:")
                # for row in possibilities:
                #     print(row)
                # print(
                #     f"permutations: {permutations} \n permutation: {permutation} \n group1: {group1} \n group2: {group2} \n difference: {difference}")
                if type(permutation) is list:
                    for position in permutation:
                        x, y = position
                        possibilities[x][y] = possibilities[x][y].intersection(
                            difference)
                else:
                    x, y = permutation
                    possibilities[x][y] = possibilities[x][y].intersection(
                        difference)
    return possibilities

#  TODO Reduce the recursive functions into a single function


def permutation_maker_recursive(arr, cnt, result):
    # Recursive function to make permutations from a given array
    arr_cpy = arr.copy()
    to_return = []

    if (cnt == 0):
        return result

    for _ in range(0, len(arr)):
        next_val = [arr_cpy.pop(0)]
        results = permutation_maker_recursive(
            arr_cpy, cnt - 1, result + next_val)
        if len(results) > 0:
            if type(results[0]) is list:
                for cur_result in results:
                    to_return.append(cur_result)
            else:
                to_return.append(results)

    return to_return


def permutation_maker(arr, cnt):
    # Base function of permutations. Makes permutations of cnt length from the values given in arr
    to_return = []
    arr_cpy = arr.copy()

    for _ in range(0, len(arr)):
        starting_val = [arr_cpy.pop(0)]
        results = permutation_maker_recursive(arr_cpy, cnt - 1, starting_val)
        for result in results:
            to_return.append(result)

    return to_return


def main():
    """ Should remove 1 from [1][1]. {'1', '5', '6'} => {'5', '6'} """
    possibilities = [
        [{'9'}, {'3'}, {'1', '4', '7'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
        [{'5', '6'}, {'1', '5', '6'}, {'1', '4', '7'}, {
            '4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
        [{'8'}, {'2'}, {'1', '4', '7'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
        [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
        [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
        [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
        [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
        [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}],
        [{'1'}, {'2'}, {'3'}, {'4'}, {'5'}, {'6'}, {'7'}, {'8'}, {'9'}]
    ]

    reducer = ForcedPositionsReducer(9, 3)
    print(reducer.reduce(possibilities))


if __name__ == "__main__":
    main()
