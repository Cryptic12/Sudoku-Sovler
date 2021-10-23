class ColumnRule:

    def isAllowed(self, board, value, position):
        _, column = position
        for row in board:
            if row[column] == value:
                return False
        return True

    def getColumnPositions(self, column: int):
        positions = []
        for row in range(9):
            positions.append((row, column))
        # print(f"Column: {positions}")
        return positions

    def getAllColumnPositions(self):
        columns = []
        for column in range(9):
            columns.append(self.getColumnPositions(column))
        return columns

    def getAffectedPositions(self, position):
        _, column = position
        affectedPositions = set(self.getColumnPositions(column))
        affectedPositions.remove(position)
        return affectedPositions
