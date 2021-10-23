class RowRule:

    def isAllowed(self, board, value, position):
        x, _ = position
        rowToTest = board[x]
        return value not in rowToTest

    def getRowPositions(self, row: int):
        positions = []
        for column in range(9):
            positions.append((row, column))
        # print(f"Row: {positions}")
        return positions

    def getAllRowPositions(self):
        rows = []
        for row in range(9):
            rows.append(self.getRowPositions(row))
        return rows

    def getAffectedPositions(self, position):
        row, _ = position
        return set(self.getRowPositions(row))
