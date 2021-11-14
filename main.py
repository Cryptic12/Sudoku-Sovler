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
from Controller.Rules.RowRule import RowRule
from Controller.Rules.ColumnRule import ColumnRule
from Controller.Rules.SquareRule import SquareRule

# Reducers
from Controller.Reducers.PossibilitiesReducer import PossibilitiesReducer
from Controller.Reducers.OnePositionReducer import OnePositionReducer
from Controller.Reducers.ForcedPositionsReducer import ForcedPositionsReducer
from Controller.Reducers.ForcedPositionsInSquareReducer import ForcedPositionsInSquareReducer


def main():
    """ Load the config"""
    CONFIG_PATH = os.path.join(os.getcwd(), 'config.cfg')

    sudoku_config = SudokuConfig(CONFIG_PATH)
    sudoku_loader = SudokuLoader(os.path.join(
        os.getcwd(), sudoku_config.get_file_name()))

    """ Setup Model """
    sudoku_model = SudokuModel(sudoku_loader.get_sudoku_board(),
                               sudoku_config.get_board_size(), sudoku_config.get_square_size())

    """ Setup Solver """
    square_rule = SquareRule(
        sudoku_config.get_square_size())
    rules = [RowRule(), ColumnRule(), square_rule]
    sudoku_rules = SudokuRules(rules)

    """ Setup Reducer """
    reducers = [OnePositionReducer(
        sudoku_config.get_board_size(), sudoku_config.get_square_size(), rules), ForcedPositionsReducer(sudoku_config.get_board_size(), sudoku_config.get_square_size()),
        ForcedPositionsInSquareReducer(square_rule)]
    possibilities_reducer = PossibilitiesReducer(reducers)

    sudoku_controller = SudokuController(
        sudoku_model, sudoku_rules, possibilities_reducer)

    """ Setup Display """
    sudoku_view = SudokuDisplay(
        sudoku_controller.solve_sudoku)
    sudoku_view.load_board(sudoku_model.get_board())

    sudoku_view_subscriber = Subscriber(sudoku_view.update)
    sudoku_model.subscribe(sudoku_view_subscriber)

    sudoku_view.start_display()

    print("Sudoku Solver Completed")


if __name__ == '__main__':
    main()
