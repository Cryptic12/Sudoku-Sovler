class ColumnRule:

    def is_allowed(self, board, value, position):
        _, column = position
        for row in board:
            if row[column] == value:
                return False
        return True

    def get_positions(self, column: int):
        positions = []
        for row in range(9):
            positions.append((row, column))
        # print(f"Column: {positions}")
        return positions

    def get_all_positions(self):
        columns = []
        for column in range(9):
            columns.append(self.get_positions(column))
        return columns

    def get_affected_positions(self, position):
        _, column = position
        affected_positions = set(self.get_positions(column))
        affected_positions.remove(position)
        return affected_positions
