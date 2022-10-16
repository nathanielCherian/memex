import logging
from re import I

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from memex.config import ConfigOption, ConfigSection, MemexConfig

from .models import Base


class BaseSession:
    def __init__(self):
        self.mc = MemexConfig()
        self.dbpath = self.mc.get(ConfigSection.DEFAULT, ConfigOption.DB_PATH)
        self.logfile = self.mc.get(ConfigSection.DEFAULT, ConfigOption.LOG_FILE)
        self.set_logging()
        self.set_logging()

    def set_logging(self):
        logging.basicConfig(
            filename=self.logfile,
            level=logging.INFO,
            format="%(asctime)s: (%(levelname)s) %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
        )

    def create_session(self):
        engine = create_engine("sqlite:///" + self.dbpath, echo=False, future=True)
        Base.metadata.create_all(engine)
        self.session = Session(engine)
        self.session.expire_on_commit = False  # HOPEFULLY THIS IS NOT A PROBLEM
