
import configparser


class ConfigLoader:

    _file_path = ""
    _config = {}

    def __init__(self, file_Path):
        self._file_path = file_Path
        self.load_config()

    # Extract that values from the config parser
    def parse_config(self, config_parser):
        config = {}
        sections = config_parser.sections()
        for section in sections:
            cur_section = config_parser[section]
            section_config = {}
            for value in cur_section:
                section_config[value] = cur_section[value]
            config[section] = section_config
        return config

    # Setup config parser and parse it
    def load_config(self):
        config_parser = configparser.ConfigParser()
        config_parser.read(self._file_path)

        self._config = self.parse_config(config_parser)

    # Returns the values extracted from the config file
    def get_config(self):
        return self._config

    # Get the file path used to extract config
    def get_file_path(self):
        return self._file_path

    # Set the file path used to extract config
    def set_file_path(self, file_path):
        self._file_path = file_path


def main():
    pass


if __name__ == '__main__':
    main()
