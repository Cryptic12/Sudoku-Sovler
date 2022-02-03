
from tkinter import *
from tkinter import ttk
from tkinter.font import Font

import math
import queue
from threading import Timer


from Model.SudokuEvents import SudokuEvents


class SudokuDisplay:

    sudoku_values = dict()

    def __init__(self, start_func, reset_func, solve_delay=1):
        self.square_size = 3
        self.start_func = start_func
        self.reset_func = reset_func
        self.stepped_solved = False
        self.update_queue = queue.SimpleQueue()
        self.queue_processing = False
        self.solve_delay = solve_delay
        self.window = Tk()
        self.setup_display()

    def setup_display(self):
        self.window.title("My Sudoku App!")
        self.window.geometry('330x400')

        self.position_font = Font(
            family="Arial", size=16, weight="bold")

        sudoku_board = Frame(borderwidth=1, relief="solid")
        sudoku_board.grid(row=0, column=0, padx=20, pady=20)

        for square in range(9):
            row = square % self.square_size
            column = math.floor(square / self.square_size)
            self.create_square(sudoku_board, square, row, column)

        sudoku_buttons = Frame()
        sudoku_buttons.grid(row=1, column=0)

        solve_button = Button(sudoku_buttons, text="Solve",
                              command=self.start_normal)
        solve_button.grid(row=0, column=0, padx=2)

        solve_slow_button = Button(sudoku_buttons, text="Solve (Slowly)",
                                   command=self.start_slow)
        solve_slow_button.grid(row=0, column=1, padx=2)

        reset_button = Button(sudoku_buttons, text="Reset",
                              command=self.reset)
        reset_button.grid(row=0, column=2, padx=2)

    def start_display(self):
        self.window.mainloop()

    def start_normal(self):
        self.stepped_solved = False
        self.start_func()

    def start_slow(self):
        self.stepped_solved = True
        self.start_func()

    def reset(self):
        self.reset_func()

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
            parent, width=2, text=value_co_ords, anchor="center", borderwidth=2, relief="solid")
        sudoku_value.configure(font=self.position_font)
        sudoku_value.grid(column=column, row=row)

        return sudoku_value

    def update(self, event):
        if event["event"] == SudokuEvents.VALUE_UPDATE:
            if self.stepped_solved:
                self.update_queue.put(event)
                if not self.queue_processing:
                    self.process_queue()
            else:
                x, y, = event["position"]
                self.update_position(x, y, event["value"])

    def process_queue(self):
        if not self.queue_processing:
            self.queue_processing = True
            t = Timer(self.solve_delay, self.process_queue)
            t.start()
        else:
            event = self.update_queue.get()
            x, y, = event["position"]
            self.update_position(x, y, event["value"])

            if self.update_queue.empty():
                self.queue_processing = False
            else:
                t = Timer(self.solve_delay, self.process_queue)
                t.start()

    def update_position(self, x, y, value):
        if value == "":
            value = " "
        self.sudoku_values[f"{x}_{y}"].configure(text=value)
