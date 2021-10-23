
import configparser


class ConfigLoader:

    _filePath = ""
    _config = {}

    def __init__(self, filePath):
        self._filePath = filePath
        self.loadConfig()

    def parseConfig(self, configParser):
        config = {}
        sections = configParser.sections()
        for section in sections:
            curSection = configParser[section]
            sectionConfig = {}
            for value in curSection:
                sectionConfig[value] = curSection[value]
            config[section] = sectionConfig
        return config

    def loadConfig(self):
        configParser = configparser.ConfigParser()
        configParser.read(self._filePath)

        self._config = self.parseConfig(configParser)

    def getConfig(self):
        return self._config

    def getFilePath(self):
        return self._filePath

    def setFilePath(self, filePath):
        self._filePath = filePath


def main():
    pass


if __name__ == '__main__':
    main()
