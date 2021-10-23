
from Other.Config.ConfigLoader import ConfigLoader


class SudokuConfig:
    _configParser = ""
    _section = ""
    _fileName = ""
    _boardSize = 0
    _squareSize = 0
    _fieldMapping = [
        ("_fileName", "FileName", "str"),
        ("_boardSize", "BoardSize", "int"),
        ("_squareSize", "SquareSize", "int"),
    ]

    def __init__(self, pathName, section="sudoku"):
        self._section = section
        self._configParser = ConfigLoader(pathName)
        self.parseConfig(self._configParser.getConfig())

    def parseConfig(self, config):
        for mapping in self._fieldMapping:
            fieldName, configName, fieldType = mapping
            self.__setattr__(fieldName, self.getValue(
                config[self._section], configName.lower(), fieldType))

    def getValue(self, section, field, type):
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

    def getFileName(self):
        return self._fileName

    def setFileName(self, fileName):
        self._fileName = fileName

    def getBoardSize(self):
        return self._boardSize

    def setBoardSize(self, boardSize):
        self._boardSize = boardSize

    def getSquareSize(self):
        return self._squareSize

    def setSquareSize(self, squareSize):
        self._squareSize = squareSize
