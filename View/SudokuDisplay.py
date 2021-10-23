from tkinter import *
from tkinter import ttk
import math

from Model.SudokuEvents import SudokuEvents


class SudokuDisplay:

    sudokuValues = dict()

    def __init__(self, startFunc):
        self.squareSize = 3
        self.startFunc = startFunc
        self.window = Tk()
        self.setupDisplay()

    def setupDisplay(self):
        self.window.title("My Sudoku App!")
        self.window.geometry('330x400')

        sudokuBoard = Frame()
        sudokuBoard.grid(column=0, row=0, padx=20, pady=20)

        for square in range(9):
            row = square % self.squareSize
            column = math.floor(square / self.squareSize)
            self.createSquare(sudokuBoard, square, row, column)

        solveButton = Button(self.window, text="Solve", command=self.startFunc)
        solveButton.grid(column=0, row=1)

    def startDisplay(self):
        self.window.mainloop()

    def loadBoard(self, sudokuBoard):
        BOARD_SIZE = len(sudokuBoard)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                self.updatePosition(x, y, sudokuBoard[x][y])

    def createSquare(self, parent, square, row, column):
        sudokuSquare = Frame(parent, borderwidth=2, relief="solid")
        sudokuSquare.grid(column=column, row=row)

        rowBase = (square % self.squareSize) * self.squareSize
        columnBase = math.floor(square / self.squareSize) * self.squareSize

        for i in range(9):
            row = i % self.squareSize
            column = math.floor(i / self.squareSize)

            valueCoOrds = f"{rowBase + row}_{columnBase + column}"
            self.sudokuValues[valueCoOrds] = self.createPosition(
                sudokuSquare, row, column, valueCoOrds)

    def createPosition(self, parent, row, column, valueCoOrds):
        sudokuValue = ttk.Label(
            parent, text=valueCoOrds, borderwidth=2, relief="solid")
        sudokuValue.grid(column=column, row=row, padx=5, pady=5)

        return sudokuValue

    def update(self, event):
        # print("Recieved event", event)

        if event["event"] == SudokuEvents.VALUE_UPDATE:
            x, y, = event["position"]
            self.updatePosition(x, y, event["value"])

    def updatePosition(self, x, y, value):
        if value == "":
            value = " "
        self.sudokuValues[f"{x}_{y}"].configure(text=value)
