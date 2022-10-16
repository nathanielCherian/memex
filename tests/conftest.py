import os
from re import I

from memex.config import ConfigOption, ConfigSection, MemexConfig

# Pytest configuration for further testing
# wipes the database before continuing


def pytest_configure():
    mc = MemexConfig()
    dbpath = mc.get(ConfigSection.DEFAULT, ConfigOption.DB_PATH) + "_test"
    mc.set(ConfigSection.DEFAULT, ConfigOption.DB_PATH, dbpath)
    mc.write()
    if os.path.exists(dbpath):
        os.remove(dbpath)
        print("Removed test database.")


def pytest_sessionfinish(session, exitstatus):
    mc = MemexConfig()
    dbpath = mc.get(ConfigSection.DEFAULT, ConfigOption.DB_PATH)[:-5]
    if os.path.exists(dbpath + "_test"):
        os.remove(dbpath + "_test")
        print("Removed test database.")
    mc.set(ConfigSection.DEFAULT, ConfigOption.DB_PATH, dbpath)
    mc.write()
