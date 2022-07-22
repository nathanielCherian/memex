from os.path import expanduser, isfile
from pathlib import Path
import configparser

CONFIG_PATH = expanduser('~')+'/.memex'

config = configparser.ConfigParser()
config['DEFAULT'] = {
    'API_PORT':3000,
    'DB_PATH':'/srv/memex.db'
}

def safe_create():
    if not isfile(CONFIG_PATH):
        with open(expanduser('~')+'/.memex', 'w') as conf_file:
            config.write(conf_file)

def read_config():
    safe_create()
    r_config = configparser.ConfigParser()
    r_config.read(CONFIG_PATH)
    return r_config


