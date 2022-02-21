
from Other.Config.ConfigLoader import ConfigLoader


class SudokuConfig:
    _config_parser = ""
    _section = ""
    _file_name = ""
    _board_size = 0
    _square_size = 0
    _field_mapping = [
        ("_file_name", "FileName", "str"),
        ("_board_size", "BoardSize", "int"),
        ("_square_size", "SquareSize", "int"),
    ]

    def __init__(self, path_name, section="sudoku"):
        self._section = section
        self._config_parser = ConfigLoader(path_name)
        self.parse_config(self._config_parser.get_config())

    # Mapthe values in the config to the defined fields
    def parse_config(self, config):
        for mapping in self._field_mapping:
            field_name, config_name, field_type = mapping
            self.__setattr__(field_name, self.get_value(
                config[self._section], config_name.lower(), field_type))

    # Filter and parse the value
    def get_value(self, section, field, type):
        if field not in section:
            return None

        value = section[field]

        if type == "int":
            try:
                value = int(value)
                return value
            except ValueError:
                raise(f"Expected field: {field} to contain an integer")

        return value

    # Get the file name
    def get_file_name(self):
        return self._file_name

    # Set the file name
    def set_file_name(self, file_name):
        self._file_name = file_name

    # Get the board size
    def get_board_size(self):
        return self._board_size

    # Set the board size
    def set_board_size(self, board_size):
        self._board_size = board_size

    # Get the square size
    def get_square_size(self):
        return self._square_size

    # Set the square size
    def set_square_size(self, square_size):
        self._square_size = square_size


def main():
    pass


if __name__ == '__main__':
    main()
