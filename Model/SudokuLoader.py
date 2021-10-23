import os


class SudokuLoader:
    # Load a Sudoku from a file

    _fileLocation = ""
    _fileLoaded = False
    _sudokuBoard = []

    def __init__(self, fileLocation):
        self._fileLocation = fileLocation

    def getFileLocation(self):
        return self._fileLocation

    def setFileLocation(self, fileLocation):
        self._fileLocation = fileLocation

    def loadFile(self):
        sudokuFile = open(self._fileLocation, "r")
        board = []

        for line in sudokuFile:
            board.append(line.rstrip().split(","))

        sudokuFile.close()

        self._sudokuBoard = board

    def getSudokuBoard(self):

        if not self._fileLoaded:
            self.loadFile()

        return self._sudokuBoard


def main():
    pass


if __name__ == "__main__":
    main()
