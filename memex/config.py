import configparser
from os.path import expanduser, isfile
from pathlib import Path
from enum import Enum

class ConfigSection(Enum):
    DEFAULT = "DEFAULT"

class ConfigOption(Enum):
    API_PORT = 'API_PORT'
    DB_PATH = 'DB_PATH'
    LOG_FILE = 'LOG_FILE'


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
        with open(self.CONFIG_PATH, 'w') as conf_file:
            self.parser.write(conf_file)
            return

    def get(self, sec, opt):
        return self.parser.get(sec.value, opt.value)

    def set(self, sec, opt, val):
        self.parser.set(sec.value, opt.value, val)
        self.write()


if __name__ == "__main__":
    mc = MemexConfig()
    mc.get(ConfigSection.DEFAULT, ConfigOption.DB_PATH)
    print(mc)


# CONFIG_PATH = expanduser("~") + "/.memexrc"

# config = configparser.ConfigParser()
# config["DEFAULT"] = {
#     "API_PORT": 3000,
#     "DB_PATH": "/tmp/memex.db",  # in produciton not gonna store in tmp
#     "LOG_FILE": "/tmp/memex.log",
# }

# # Reserved for plugins
# config["plugins"] = {}


# def safe_create():
#     if not isfile(CONFIG_PATH):
#         with open(CONFIG_PATH, "w") as conf_file:
#             config.write(conf_file)


# def edit_config(sec, var, val):
#     config.set(sec, var, val)

# def read_config():
#     safe_create()
#     r_config = configparser.ConfigParser()
#     r_config.read(CONFIG_PATH)
#     return r_config
