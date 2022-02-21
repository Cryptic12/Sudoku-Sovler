import os
from Other.Config.SudokuConfig import SudokuConfig

#  Model
from Model.SudokuLoader import SudokuLoader
from Model.SudokuModel import SudokuModel

# View
from View.SudokuDisplay import SudokuDisplay

#  Controller
from Controller.SudokuController import SudokuController

# Subscriber
from Other.Subscriber import Subscriber

# Rules
from Controller.Rules.SudokuRules import SudokuRules
from Controller.Rules.Conditions.Conditions import UniqueCondition
from Controller.Rules.Rules import RowRule, ColumnRule, SquareRule

# Reducers
from Controller.Reducers.PossibilitiesReducer import PossibilitiesReducer
from Controller.Reducers.Reducers import OnePositionReducer, ForcedPositionsReducer, ForcedPositionsInSquareReducer


def main():
    """ Load the config"""
    CONFIG_PATH = os.path.join(os.getcwd(), 'config.cfg')
    sudoku_config = SudokuConfig(CONFIG_PATH)

    """ Setup Model """
    sudoku_model = SudokuModel(
        sudoku_config.get_board_size(), sudoku_config.get_square_size())

    if sudoku_config.get_file_name():
        sudoku_loader = SudokuLoader(os.path.join(
            os.getcwd(), sudoku_config.get_file_name()))

    """ Setup Solver """
    unique_condition = UniqueCondition()

    ROW_RULE = RowRule(sudoku_config.get_board_size(), [unique_condition])
    COLUMN_RULE = ColumnRule(sudoku_config.get_board_size(),
                             [unique_condition])
    SQUARE_RULE = SquareRule(sudoku_config.get_board_size(),
                             sudoku_config.get_square_size(), [unique_condition])
    ALL_RULES = [ROW_RULE, COLUMN_RULE, SQUARE_RULE]
    sudoku_rules = SudokuRules(ALL_RULES)

    """ Setup Reducer """
    REDUCERS = []

    REDUCERS.append(OnePositionReducer(
        sudoku_config.get_board_size(), sudoku_config.get_square_size(), ALL_RULES))
    REDUCERS.append(ForcedPositionsReducer(
        sudoku_config.get_board_size(), sudoku_config.get_square_size(), ALL_RULES))
    REDUCERS.append(ForcedPositionsInSquareReducer(
        SQUARE_RULE, [ROW_RULE, COLUMN_RULE]))

    possibilities_reducer = PossibilitiesReducer(REDUCERS)

    """ Setup Controller """
    sudoku_controller = SudokuController(
        sudoku_model, sudoku_loader, sudoku_rules, possibilities_reducer)

    """ Setup Display """
    sudoku_view = SudokuDisplay(
        sudoku_config.get_square_size(), sudoku_controller.solve_sudoku, sudoku_controller.reset_board)

    sudoku_view_subscriber = Subscriber(sudoku_view.update)
    sudoku_model.subscribe(sudoku_view_subscriber)

    sudoku_controller.reset_board()
    sudoku_view.start_display()

    print("Exiting")


if __name__ == '__main__':
    main()
