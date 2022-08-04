import os

from memex.config import ConfigOption, ConfigSection, MemexConfig


def pytest_configure():
    mc = MemexConfig()
    dbpath = mc.get(ConfigSection.DEFAULT, ConfigOption.DB_PATH)
    if os.path.exists(dbpath):
        os.remove(dbpath)
        print("Removed database.")
