class RowRule:

    def is_allowed(self, board, value, position):
        x, _ = position
        row_to_test = board[x]
        return value not in row_to_test

    def get_positions(self, row: int):
        positions = []
        for column in range(9):
            positions.append((row, column))

        return positions

    def get_all_positions(self):
        rows = []
        for row in range(9):
            rows.append(self.get_positions(row))
        return rows

    def get_affected_positions(self, position):
        row, _ = position
        affected_positions = set(self.get_positions(row))
        affected_positions.remove(position)
        return affected_positions
