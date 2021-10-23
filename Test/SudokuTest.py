from dataclasses import dataclass


@dataclass
class SudokuTest():
    """ 
    startingValues = The changes to be made to a given row/column/square 
    modifiedPositions = The positions where we expect changes
    modifiedValues = The values we expect the changed positions to contain
    """
    startingValues: list
    modifiedPositions: list
    modifiedValues: list
