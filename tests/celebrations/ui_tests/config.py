import configparser
import os

class Config:
    """Class to handle configuration files."""
    _config = configparser.ConfigParser()

    @classmethod
    def load(cls, filename="config.ini"):
        """Load the configuration file."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"{filename} not found.")
        cls._config.read(filename)

    @classmethod
    def get_section(cls, section):
        """Get a specific section from the configuration file."""
        if not cls._config.has_section(section):
            raise configparser.NoSectionError(f"Section {section} not found in the configuration file.")
        return dict(cls._config.items(section))

# Load the config file when the module is imported
try:
    Config.load()
except (FileNotFoundError, configparser.NoSectionError) as e:
    print(e)