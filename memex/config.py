from os.path import expanduser, isfile
from pathlib import Path
import configparser

from memex.utils import load_module

CONFIG_PATH = expanduser("~") + "/.memexrc"

config = configparser.ConfigParser()
config["DEFAULT"] = {
    "API_PORT": 3000,
    "DB_PATH": "/tmp/memex.db",  # in produciton not gonna store in tmp
    "LOG_FILE": "/tmp/memex.log",
}

# Reserved for plugins
config["plugins"] = {}


def safe_create():
    if not isfile(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as conf_file:
            config.write(conf_file)


def read_config():
    safe_create()
    r_config = configparser.ConfigParser()
    r_config.read(CONFIG_PATH)
    return r_config
