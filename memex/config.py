import configparser
from enum import Enum
from os.path import expanduser, isfile
from pathlib import Path


class ConfigSection(Enum):
    DEFAULT = "DEFAULT"


class ConfigOption(Enum):
    API_PORT = "API_PORT"
    DB_PATH = "DB_PATH"
    TEST_DB_PATH = "TEST_DB_PATH"
    LOG_FILE = "LOG_FILE"
    REMOTE = "REMOTE"
    TOKEN = "TOKEN"


class MemexConfig:
    CONFIG_PATH = expanduser("~") + "/.memexrc"

    def __init__(self) -> None:
        if not isfile(self.CONFIG_PATH):
            self.parser = self.default_parser()
            self.write()
        self.parser = configparser.ConfigParser()
        self.parser.read(self.CONFIG_PATH)
        return

    def default_parser(self):
        parser = configparser.ConfigParser()
        parser[ConfigSection.DEFAULT.value] = {
            ConfigOption.API_PORT.value: 3000,
            ConfigOption.DB_PATH.value: "/tmp/memex.db",  # in produciton not gonna store in tmp
            ConfigOption.LOG_FILE.value: "/tmp/memex.log",
        }
        return parser

    def write(self):
        with open(self.CONFIG_PATH, "w") as conf_file:
            self.parser.write(conf_file)
            return

    def get(self, sec, opt, fallback=None):
        return self.parser.get(sec.value, opt.value, fallback=fallback)

    def set(self, sec, opt, val):
        self.parser.set(sec.value, opt.value, val)
        self.write()


if __name__ == "__main__":
    mc = MemexConfig()
    mc.get(ConfigSection.DEFAULT, ConfigOption.DB_PATH)
    print(mc)
