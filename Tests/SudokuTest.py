from dataclasses import dataclass


@dataclass
class SudokuTest():
    """ 
    starting_values = The changes to be made to a given row/column/square 
    modified_positions = The positions where we expect changes
    modified_values = The values we expect the changed positions to contain
    """
    starting_values: list
    reductions: dict


def main():
    pass


if __name__ == '__main__':
    main()
