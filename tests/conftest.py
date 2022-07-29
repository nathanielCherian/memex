import os

from memex.config import read_config


def pytest_configure():
    dbpath = read_config()["DEFAULT"]["DB_PATH"]
    if os.path.exists(dbpath):
        os.remove(dbpath)
        print("Removed database.")
