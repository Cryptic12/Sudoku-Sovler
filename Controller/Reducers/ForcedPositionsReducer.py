import math


class ForcedPositionsReducer():
    """ Identifies sets of positions in a given row/column/square where a subset of values are forced to be placed into """

    def __init__(self, boardSize, squareSize):
        self.boardSize = boardSize
        self.squareSize = squareSize

    def reduce(self, possibilities):
        possibilities = self.reduceByRow(possibilities)
        possibilities = self.reduceByColumn(possibilities)
        return self.reduceBySquare(possibilities)

    def reduceByRow(self, possibilities):
        for row in range(self.boardSize):

            # For each position, count the number of times each value appears
            positions = []
            for column in range(self.boardSize):

                if len(possibilities[row][column]) <= 1:
                    continue

                positions.append((row, column))

            # print(f"Row: {row}")
            possibilities = reducePositionsOuter(possibilities, positions)

        return possibilities

    def reduceByColumn(self, possibilities):
        for column in range(self.boardSize):

            # For each position, count the number of times each value appears
            positions = []
            for row in range(self.boardSize):

                if len(possibilities[row][column]) <= 1:
                    continue

                positions.append((row, column))

            # print(f"Column: {column}")
            possibilities = reducePositionsOuter(possibilities, positions)

        return possibilities

    def reduceBySquare(self, possibilities):
        SQUARE_SIZE = self.squareSize
        SQUARE_COUNT = int(self.boardSize / SQUARE_SIZE) ** 2

        for square in range(0, SQUARE_COUNT):

            rowBase = (square % SQUARE_SIZE) * SQUARE_SIZE
            columnBase = math.floor(square / SQUARE_SIZE) * SQUARE_SIZE

            # For each position, count the number of times each value appears
            positions = []
            for x in range(0, SQUARE_SIZE):
                curRow = rowBase + x
                for y in range(0, SQUARE_SIZE):
                    curColumn = columnBase + y

                    if len(possibilities[curRow][curColumn]) <= 1:
                        continue

                    positions.append((curRow, curColumn))

            # print(f"Square: {square}")
            possibilities = reducePositionsOuter(possibilities, positions)

        return possibilities


def reducePositionsOuter(possibilities, positions):
    valueCounts = calculateValueCounts(possibilities, positions)

    if len(valueCounts) < 1:
        return possibilities

    return doPermutations(possibilities, positions, valueCounts)


def calculateValueCounts(possibilities, positions):
    valueCounts = {}

    for position in positions:
        row, column = position
        possibility = possibilities[row][column]
        for value in possibility:
            count = valueCounts.get(value)
            if count == None:
                valueCounts[value] = 1
            else:
                valueCounts[value] = count + 1

    return valueCounts


def doPermutations(possibilities, positions, valueCounts):

    valueCountsMin = min(valueCounts.values())

    # Check till 2 fewer than the total number of unsolved spaces
    for i in range(valueCountsMin, len(positions) - 1):
        permutations = permutationMaker(positions, i)

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
                print(
                    f"~~~ {i} ~~~ \n possibilities:")
                for row in possibilities:
                    print(row)
                print(
                    f"permutations: {permutations} \n permutation: {permutation} \n group1: {group1} \n group2: {group2} \n difference: {difference}")
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


def permutationMakerRecursive(arr, cnt, result):
    # Recursive function to make permutations from a given array
    arrCpy = arr.copy()
    toReturn = []

    if (cnt == 0):
        return result

    for _ in range(0, len(arr)):
        nextVal = [arrCpy.pop(0)]
        results = permutationMakerRecursive(arrCpy, cnt - 1, result + nextVal)
        if len(results) > 0:
            if type(results[0]) is list:
                for curResult in results:
                    toReturn.append(curResult)
            else:
                toReturn.append(results)

    return toReturn


def permutationMaker(arr, cnt):
    # Base function of permutations. Makes permutations of cnt length from the values given in arr
    toReturn = []
    arrCpy = arr.copy()

    for _ in range(0, len(arr)):
        startingVal = [arrCpy.pop(0)]
        results = permutationMakerRecursive(arrCpy, cnt - 1, startingVal)
        for result in results:
            toReturn.append(result)

    return toReturn


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
