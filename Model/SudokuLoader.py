import os


class SudokuLoader:
    # Load a Sudoku from a file

    _file_location = ""
    _file_loaded = False
    _sudoku_board = []

    def __init__(self, file_location):
        self._file_location = file_location

    # Returns the path of the file
    def get_file_location(self):
        return self._file_location

    # Sets the file path
    def set_file_location(self, file_location):
        self._file_location = file_location

    # Loads the board stored in the current file
    def load_file(self):
        with open(self._file_location, "r") as sudoku_file:
            board = []
            for line in sudoku_file:
                board.append(line.rstrip().split(","))
            self._sudoku_board = board

    # Returns the loaded board
    def get_sudoku_board(self):

        if not self._file_loaded:
            self.load_file()

        return self._sudoku_board


def main():
    pass


if __name__ == "__main__":
    main()
