import os
import math
import sys

# FILE_TO_SOLVE = "../input/7_5_21.txt"
FILE_TO_SOLVE = "Input/toSolve2.txt"
# FILE_TO_SOLVE = "../input/toSolveAdv.txt"
GRID_WIDTH = 23
EMPTY_CHAR = "-"
ROW_COUNT = 9
COLUMN_COUNT = 9
SQUARE_COUNT = 9
SQUARE_SIZE = 3
DEBUG = False

# Debug function


def breaker():
    test = 'a' + 1

# Functions to get relevant values from board


def getValueList(value, valueList):
    if type(value) is list:
        valueList += value
    elif value != '':
        valueList.append(value)

    return valueList


def getRowValues(row, board):
    # For a given row, return all the used values
    toReturn = []
    for value in board[row]:
        toReturn = getValueList(value, toReturn)
    return toReturn


def getColumnValues(column, board):
    # For a given column, return all the used values
    toReturn = []
    for row in range(0, COLUMN_COUNT):
        value = board[row][column]
        toReturn = getValueList(value, toReturn)
    return toReturn


def getSquareValues(square, board):
    # For a given square, return all the used values
    toReturn = []
    columnPos = math.floor(square / SQUARE_SIZE) * SQUARE_SIZE
    rowPos = (square % SQUARE_SIZE) * SQUARE_SIZE
    for x in range(columnPos, columnPos + SQUARE_SIZE):
        curRow = board[x]
        for y in range(rowPos, rowPos + SQUARE_SIZE):
            value = curRow[y]
            toReturn = getValueList(value, toReturn)
    return toReturn

# Outputs the current state of the board


def drawBorder():
    print("=" * GRID_WIDTH)


def drawRow(row, board):
    # Outputs the given row into the terminal
    toPrint = ""
    for column in range(0, COLUMN_COUNT):
        if column % SQUARE_SIZE == 0:
            toPrint += "|"

        num = board[row][column]
        if type(num) is str and num != '':
            toPrint += num
        else:
            toPrint += EMPTY_CHAR
        toPrint += "|"

        if column % SQUARE_SIZE == SQUARE_SIZE - 1:
            toPrint += " "
    print(toPrint)


def drawBoard(board):
    # Draws the entire board
    drawBorder()
    for x in range(0, ROW_COUNT):

        drawRow(x, board)
        if (x % SQUARE_SIZE == SQUARE_SIZE - 1 and x != ROW_COUNT - 1):
            print("")

    drawBorder()


# Solve the sudoku


def solvedCount(board):
    # Counts the number of solved positions
    total = 0
    for row in range(0, ROW_COUNT):
        for column in range(0, COLUMN_COUNT):
            if board[row][column] != '':
                total += 1

    return total


def makePossibilityKey(x, y):
    return str(x) + '_' + str(y)


def possibilityExists(key, possibilitiesKeys):
    return key in possibilitiesKeys


def compareArraySets(arr1, arr2):
    # Returns the values which are present in the first array set(s) but not in the second array set(s)

    union1 = set()
    union2 = set()

    for set1 in arr1:
        union1 = union1.union(set1)

    for set2 in arr2:
        union2 = union2.union(set2)

    return union1.difference(union2)

# Permutation functions


def permutationMakerRecursive(arr, cnt, result):
    # Recursive function to make permutations from a given array
    arrCpy = arr.copy()
    toReturn = []

    if (cnt == 0):
        return result

    for i in range(0, len(arr)):
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

    print("Permutation", arr)

    for i in range(0, len(arr)):
        startingVal = [arrCpy.pop(0)]
        results = permutationMakerRecursive(arrCpy, cnt - 1, startingVal)
        for result in results:
            toReturn.append(result)

    return toReturn


def solveBoardBySquareAdv(possibilities):

    # Once complete, should be able to merge logic into solveBoardBySquare()
    for square in range(0, SQUARE_COUNT):

        rowBase = (square % SQUARE_SIZE) * SQUARE_SIZE
        columnBase = math.floor(square / SQUARE_SIZE) * SQUARE_SIZE

        valueCounts = {}
        valueCountKeys = valueCounts.keys()
        possibilitiesArray = []
        possibilitiesKeys = possibilities.keys()
        curSqrPossibilities = []

        for x in range(0, SQUARE_SIZE):
            curRow = rowBase + x
            for y in range(0, SQUARE_SIZE):
                curColumn = columnBase + y
                possibilityKey = makePossibilityKey(curRow, curColumn)
                if possibilityKey in possibilitiesKeys:
                    valueSet = set()
                    curSqrPossibilities.append(possibilityKey)
                    for value in possibilities[possibilityKey]:
                        if value in valueCountKeys:
                            valueCounts[value] = valueCounts[value] + 1
                        else:
                            valueCounts[value] = 1
                        valueSet.add(value)
                    possibilitiesArray.append(valueSet)

        valueCountsMin = None
        valueCountsMax = None

        for key in valueCountKeys:
            count = valueCounts[key]
            if (not valueCountsMin or count < valueCountsMin):
                valueCountsMin = count
            if (not valueCountsMax or count > valueCountsMax):
                valueCountsMax = count

        # Check till 2 fewer than the total number of unsolved spaces
        if (valueCountsMin or valueCountsMax):
            for i in range(valueCountsMin, len(possibilitiesArray) - 1):

                permutations = permutationMaker(curSqrPossibilities, i)
                for permutation in permutations:
                    group1 = set()
                    group2 = set()
                    for curSqrPossibility in curSqrPossibilities:
                        if curSqrPossibility in permutation:
                            # Values that are in all of the positions
                            if group1:
                                group1 = group1.intersection(
                                    possibilities[curSqrPossibility])
                            else:
                                group1 = group1.union(
                                    possibilities[curSqrPossibility])
                        else:
                            # Values found in any of the other positions
                            group2 = group2.union(
                                possibilities[curSqrPossibility])

                    difference = group1.difference(group2)
                    if len(difference) == i:
                        #print("permutation", permutation)
                        if type(permutation) is list:
                            for position in permutation:
                                possibilities[position] = list(difference)
                        else:
                            possibilities[permutation] = list(difference)
    return possibilities


def solveBoardBySquare(board, possibilities):
    # For each square and for each possible number check if there is only one place in the square where it could go

    drawBoard(board)

    for square in range(0, SQUARE_COUNT):

        valueCounts = {}
        keys = valueCounts.keys()
        possibilitiesKeys = possibilities.keys()

        rowBase = (square % SQUARE_SIZE) * SQUARE_SIZE
        columnBase = math.floor(square / SQUARE_SIZE) * SQUARE_SIZE

        # Count the occurances of each value within the square
        for x in range(0, SQUARE_SIZE):
            curRow = rowBase + x
            for y in range(0, SQUARE_SIZE):
                curColumn = columnBase + y
                possibilityKey = makePossibilityKey(curRow, curColumn)
                if possibilityKey in possibilitiesKeys:
                    for value in possibilities[possibilityKey]:
                        if value in keys:
                            valueCounts[value] = valueCounts[value] + 1
                        else:
                            valueCounts[value] = 1
                else:
                    valueCounts[board[curRow][curColumn]] = 2

        # Identify all values which only appear once
        solvableValues = set()
        for key in keys:
            if valueCounts[key] == 1:
                solvableValues.add(key)

        # Solve the board based on the found values
        for x in range(0, SQUARE_SIZE):
            curRow = rowBase + x
            for y in range(0, SQUARE_SIZE):
                curColumn = columnBase + y
                possibilityKey = makePossibilityKey(curRow, curColumn)
                if possibilityKey in possibilitiesKeys:
                    for value in possibilities[possibilityKey]:
                        if value in solvableValues:
                            board[curRow][curColumn] = value

    return board


def solveBoardByLine(board, possibilities):
    # Checks if there is only one position in a line (row or column) that can contain a particular value.
    # This is very similar to the solveBoardBySquare func

    # Solve by row
    for row in range(0, ROW_COUNT):

        valueCounts = {}
        keys = valueCounts.keys()
        possibilitiesKeys = possibilities.keys()

        # Count the occurances of each value within the row
        for column in range(0, COLUMN_COUNT):
            possibilityKey = makePossibilityKey(row, column)
            if possibilityKey in possibilitiesKeys:
                for value in possibilities[possibilityKey]:
                    if value in keys:
                        valueCounts[value] = valueCounts[value] + 1
                    else:
                        valueCounts[value] = 1
            else:
                valueCounts[board[row][column]] = 2

        # Identify all values which only appear once
        solvableValues = set()
        for key in keys:
            if valueCounts[key] == 1:
                solvableValues.add(key)

        # Solve the board based on the found values
        for column in range(0, COLUMN_COUNT):
            possibilityKey = makePossibilityKey(row, column)
            if possibilityKey in possibilitiesKeys:
                for value in possibilities[possibilityKey]:
                    if value in solvableValues:
                        board[row][column] = value

    # Solve by column
    for column in range(0, COLUMN_COUNT):

        valueCounts = {}
        keys = valueCounts.keys()
        possibilitiesKeys = possibilities.keys()

        # Count the occurances of each value within the column
        for row in range(0, ROW_COUNT):
            possibilityKey = makePossibilityKey(row, column)
            if possibilityKey in possibilitiesKeys:
                for value in possibilities[possibilityKey]:
                    if value in keys:
                        valueCounts[value] = valueCounts[value] + 1
                    else:
                        valueCounts[value] = 1
            else:
                valueCounts[board[row][column]] = 2

        # Identify all values which only appear once
        solvableValues = set()
        for key in keys:
            if valueCounts[key] == 1:
                solvableValues.add(key)

        # Solve the board based on the found values
        for row in range(0, ROW_COUNT):
            possibilityKey = makePossibilityKey(row, column)
            if possibilityKey in possibilitiesKeys:
                for value in possibilities[possibilityKey]:
                    if value in solvableValues:
                        board[row][column] = value

    return board


def solveBoard(board):
    # Solves the board by computing which possible values a position can have based on what values are in
    # corresponding square, row, and column
    rows = {}
    columns = {}
    squares = {}
    possibilities = {}
    valueSolved = False

    # Fetch the values from each of the rows, columns, and squares
    for i in range(0, ROW_COUNT):
        rows[i] = getRowValues(i, board)
        columns[i] = getColumnValues(i, board)
        squares[i] = getSquareValues(i, board)

    # For each position, find all possible values
    for curRow in range(0, ROW_COUNT):
        for curColumn in range(0, COLUMN_COUNT):
            if type(board[curRow][curColumn]) is list or board[curRow][curColumn] == '':

                curSquare = math.floor(curColumn / SQUARE_SIZE) + \
                    (math.floor(curRow / SQUARE_SIZE) * SQUARE_SIZE)
                row = rows[curRow]
                column = columns[curColumn]
                square = squares[curSquare]

                # Find all the possible values
                possibleValues = []
                for value in range(1, ROW_COUNT + 1):
                    value = str(value)
                    if (value not in row and value not in column and value not in square):
                        possibleValues.append(value)

                if len(possibleValues) == 1:
                    board[curRow][curColumn] = possibleValues[0]
                    valueSolved = True
                else:
                    possibilities[str(curRow) + '_' +
                                  str(curColumn)] = possibleValues

    if (not valueSolved):
        print("No values solved. Attemping advanced solver")
        drawBoard(board)
        board = solveBoardAdv(board, possibilities)

    return board


def solveBoardAdv(board, possibilities):
    # Attempts to reduce the posilibilites of a position by identifying positions in a row or column in another square
    # which must contain a given value based on logical conclusions from other values in the grid

    # possibilities contains a dictionary with the key being 'x_y' and the value being a list of the possible values for that position
    # print(possibilities)
    # print(possibilities.keys())

    possibilities = solveBoardBySquareAdv(possibilities)

    # Loop through each of the squares
    possibilitiesKeys = possibilities.keys()
    for square in range(0, SQUARE_COUNT):
        # for square in range(2, 3):  # Only look at square 2
        rowBase = math.floor(square / 3) * 3
        columnBase = (square % 3) * 3

        # Identify all of the unsolved values for the square
        keys = []
        for x in range(0, SQUARE_SIZE):
            for y in range(0, SQUARE_SIZE):
                xPos = str(rowBase + x)
                yPos = str(columnBase + y)
                key = makePossibilityKey(xPos, yPos)
                if possibilityExists(key, possibilitiesKeys):
                    keys.append(key)

        # Loop of keys and do something interesting i don't know lol
        for key in keys:
            pass

        # Loop over the rows and columns and check if any rows or columns contain a given value
        rowValues = []
        columnValues = []

        for first in range(0, SQUARE_SIZE):
            rowValue = set({})
            columnValue = set({})
            for second in range(0, SQUARE_SIZE):
                # Check by row
                rowKey = makePossibilityKey(
                    rowBase + first, columnBase + second)
                if possibilityExists(rowKey, possibilitiesKeys):
                    for xValue in possibilities[rowKey]:
                        rowValue.add(xValue)
                # Check by column
                columnKey = makePossibilityKey(
                    rowBase + second, columnBase + first)
                if possibilityExists(columnKey, possibilitiesKeys):
                    for yValue in possibilities[columnKey]:
                        columnValue.add(yValue)

            rowValues.append(rowValue)
            columnValues.append(columnValue)

        # Check if any of the rows/columns contain values that the others don't
        for i in range(0, SQUARE_SIZE):
            # print(i)
            # print(rowValues)
            # print(columnValues)

            rowSet = rowValues[i]
            columnSet = columnValues[i]
            rowDifferences = []
            columnDifferences = []
            uniqueRowValues = set()
            uniqueColumnValues = set()

            # Populate set with all possible values
            for j in range(1, SQUARE_SIZE ** 2 + 1):
                uniqueRowValues.add(str(j))
                uniqueColumnValues.add(str(j))

            # Identify what values each line doesn't contain
            for j in range(0, SQUARE_SIZE):
                if i != j:
                    rowDifferences.append(rowSet.difference(rowValues[j]))
                    columnDifferences.append(
                        columnSet.difference(columnValues[j]))

            # Identify any values that each of the other lines don't contain
            for j in range(0, len(rowDifferences)):
                uniqueRowValues.intersection_update(rowDifferences[j])

            for j in range(0, len(columnDifferences)):
                uniqueColumnValues.intersection_update(
                    columnDifferences[j])

            #
            #   Something is wrong with the logic around here. It is removing values that it shouldn't be :(
            #

            if len(uniqueRowValues) > 0:
                # Remove values from the possibilities
                for columnPos in range(0, COLUMN_COUNT):
                    if (columnPos < columnBase or columnPos >= columnBase + 3):
                        key = makePossibilityKey(
                            rowBase + i, columnPos)
                        if possibilityExists(key, possibilitiesKeys):
                            values = possibilities[key]
                            # print('Row: Updating key ' + key +
                            #     ' to ', values, uniqueRowValues, square)
                            for toRemove in uniqueRowValues:
                                if toRemove in values:
                                    values.remove(toRemove)
                            possibilities[key] = values

            if len(uniqueColumnValues) > 0:
                # Remove values from the possibilities
                for rowPos in range(0, ROW_COUNT):
                    if (rowPos < rowBase or rowPos >= rowBase + 3):
                        key = makePossibilityKey(
                            rowPos, columnBase + i)
                        if possibilityExists(key, possibilitiesKeys):
                            values = possibilities[key]
                            # print('Column: Updating key ' + key +
                            #  ' to ', values, uniqueColumnValues, square)
                            for toRemove in uniqueColumnValues:
                                if toRemove in values:
                                    values.remove(toRemove)
                            possibilities[key] = values

    for key in possibilitiesKeys:
        if len(possibilities[key]) == 1:
            print("Solving " + key + " with possibilities of ",
                  possibilities[key])

            positions = key.split("_")
            xPos = int(positions[0])
            yPos = int(positions[1])
            board[xPos][yPos] = possibilities[key][0]

    # breaker()

    board = solveBoardBySquare(board, possibilities)
    board = solveBoardByLine(board, possibilities)

    print(possibilities)

    return board


# Allows the user to input the current board


def inputSudoku():
    # Input the sudoku via the terminal
    curRow = 0
    board = []

    while (curRow < COLUMN_COUNT):
        square = input("Please input line %d:" % (curRow + 1))
        board.append(square.split(","))
        curRow += 1

    print("All rows have been inputed!")

    return board


def readSudoku():
    # Input the sudoku via a text file
    sudokuFile = open(os.path.join(os.path.dirname(
        __file__), FILE_TO_SOLVE), "r")
    board = []

    for line in sudokuFile:
        input = line.rstrip().split(",")
        if (len(input) != COLUMN_COUNT):
            print(input)
            sys.exit("Current line had the incorrect number of values")
        board.append(input)

    sudokuFile.close()

    print("All rows have been loaded!")

    return board


def main():
    # board = inputSudoku()
    board = readSudoku()
    boardSolved = False
    iterations = 0
    prevCnt = 0
    drawBoard(board)

    while not boardSolved:
        board = solveBoard(board)
        solvedCnt = solvedCount(board)
        iterations += 1

        if solvedCnt == ROW_COUNT * COLUMN_COUNT:
            boardSolved = True
        elif prevCnt == solvedCnt:
            boardSolved = True
            print("Unable to progress with %s squares solved" % solvedCnt)

        if DEBUG == True:
            boardSolved = True

        prevCnt = solvedCnt
        # drawBoard(board)

    print("Finished in %s iterations!" % iterations)
    drawBoard(board)


if __name__ == '__main__':
    main()
    # test = [{1, 2, 3}, {2, 3, 4}, {3, 4, 5}, {4, 5, 6}, {5, 6, 7}]
    # test = [1, 2, 3, 4, 5]
    # abc(positions, remainder, count)

    # compareArraySets([{1, 2, 3}, {2, 3, 4}], [{3, 4, 5}, {4, 5, 6}, {5, 6, 7}])

    # print(permutationMaker(test, 4))
