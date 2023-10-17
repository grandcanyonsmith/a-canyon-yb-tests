import configparser


class Config:
    """Class to handle configuration files."""
    _config = configparser.ConfigParser()

    @classmethod
    def load(cls, filename="config.ini"):
        """Load the configuration file."""
        cls._config.read(filename)

    @classmethod
    def get_section(cls, section):
        """Get a specific section from the configuration file."""
        try:
            return dict(cls._config.items(section))
        except configparser.NoSectionError:
            return None


# Load the config file when the module is imported
Config.load()