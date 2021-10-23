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

    sudokuConfig = SudokuConfig(CONFIG_PATH)
    sudokuLoader = SudokuLoader(os.path.join(
        os.getcwd(), sudokuConfig.getFileName()))

    """ Setup Model """
    sudokuModel = SudokuModel(sudokuLoader.getSudokuBoard(),
                              sudokuConfig.getBoardSize(), sudokuConfig.getSquareSize())

    """ Setup Solver """
    squareRule = SquareRule(
        sudokuConfig.getSquareSize())
    rules = [RowRule(), ColumnRule(), squareRule]
    sudokuRules = SudokuRules(rules)

    """ Setup Reducer """
    reducers = [OnePositionReducer(
        sudokuConfig.getBoardSize(), sudokuConfig.getSquareSize(), rules), ForcedPositionsReducer(sudokuConfig.getBoardSize(), sudokuConfig.getSquareSize()),
        ForcedPositionsInSquareReducer(squareRule)]
    possibilitiesReducer = PossibilitiesReducer(reducers)

    sudokuController = SudokuController(
        sudokuModel, sudokuRules, possibilitiesReducer)

    """ Setup Display """
    sudokuView = SudokuDisplay(
        sudokuController.solveSudoku)
    sudokuView.loadBoard(sudokuModel.getBoard())

    sudokuViewSubscriber = Subscriber(sudokuView.update)
    sudokuModel.subscribe(sudokuViewSubscriber)

    sudokuView.startDisplay()

    print("Sudoku Solver Completed")


if __name__ == '__main__':
    main()
