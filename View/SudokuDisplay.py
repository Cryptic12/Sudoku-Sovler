
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.dialog import DIALOG_ICON
from tkinter.font import Font

import math
import queue
from threading import Timer


from Model.SudokuEvents import SudokuEvents


class SudokuDisplay:

    sudoku_values = dict()
    buttons = []

    def __init__(self, square_size, start_func, reset_func, solve_delay=1):

        self.square_size = square_size
        self.start_func = start_func
        self.reset_func = reset_func

        # State for stepped solving
        self.stepped_solved = False
        self.queue_processing = False
        self.update_queue = queue.SimpleQueue()
        self.solve_delay = solve_delay

        # Initiate display
        self.window = Tk()
        self.setup_display()

    def setup_display(self):
        self.window.title("My Sudoku App!")
        self.window.geometry('310x360')
        self.window.resizable(0, 0)

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

        self.buttons = [solve_button, solve_slow_button, reset_button]

    def start_display(self):
        self.window.mainloop()

    def start_normal(self):
        for button in self.buttons:
            button.configure(state=DISABLED)
        self.was_solved = self.start_func()
        self.sudoku_completed()

    def start_slow(self):
        self.stepped_solved = True
        for button in self.buttons:
            button.configure(state=DISABLED)
        self.was_solved = self.start_func()
        self.process_queue()

    def sudoku_completed(self):
        for button in self.buttons:
            button.configure(state=ACTIVE)

        message = ""
        if (self.was_solved):
            message = "Sudoku Solved!"
        else:
            message = "Sudoku Not Solved :("

        messagebox.showinfo(title=None, message=message)

    def reset(self):
        self.stepped_solved = False
        self.was_solved = False
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
                self.sudoku_completed()
            else:
                t = Timer(self.solve_delay, self.process_queue)
                t.start()

    def update_position(self, x, y, value):
        if value == "":
            value = " "
        self.sudoku_values[f"{x}_{y}"].configure(text=value)
