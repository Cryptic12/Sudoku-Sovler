from tkinter import *
from tkinter import ttk
import math

from Model.SudokuEvents import SudokuEvents


class SudokuDisplay:

    sudoku_values = dict()

    def __init__(self, start_func):
        self.square_size = 3
        self.start_func = start_func
        self.window = Tk()
        self.setup_display()

    def setup_display(self):
        self.window.title("My Sudoku App!")
        self.window.geometry('330x400')

        sudoku_board = Frame()
        sudoku_board.grid(column=0, row=0, padx=20, pady=20)

        for square in range(9):
            row = square % self.square_size
            column = math.floor(square / self.square_size)
            self.create_square(sudoku_board, square, row, column)

        solve_button = Button(self.window, text="Solve",
                              command=self.start_func)
        solve_button.grid(column=0, row=1)

    def start_display(self):
        self.window.mainloop()

    def load_board(self, sudoku_board):
        BOARD_SIZE = len(sudoku_board)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                self.update_position(x, y, sudoku_board[x][y])

    def create_square(self, parent, square, row, column):
        sudoku_square = Frame(parent, borderwidth=2, relief="solid")
        sudoku_square.grid(column=column, row=row)

        ROW_BASE = (square % self.square_size) * self.square_size
        COLUMN_BASE = math.floor(square / self.square_size) * self.square_size

        for i in range(9):
            row = i % self.square_size
            column = math.floor(i / self.square_size)

            value_co_ords = f"{ROW_BASE + row}_{COLUMN_BASE + column}"
            self.sudoku_values[value_co_ords] = self.create_position(
                sudoku_square, row, column, value_co_ords)

    def create_position(self, parent, row, column, value_co_ords):
        sudoku_value = ttk.Label(
            parent, text=value_co_ords, borderwidth=2, relief="solid")
        sudoku_value.grid(column=column, row=row, padx=5, pady=5)

        return sudoku_value

    def update(self, event):
        # print("Recieved event", event)

        if event["event"] == SudokuEvents.VALUE_UPDATE:
            x, y, = event["position"]
            self.update_position(x, y, event["value"])

    def update_position(self, x, y, value):
        if value == "":
            value = " "
        self.sudoku_values[f"{x}_{y}"].configure(text=value)
