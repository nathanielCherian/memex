import logging
from cgitb import text
from re import I

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from memex.config import ConfigOption, ConfigSection, MemexConfig

from .models import Base


class BaseManager:
    def __init__(self):
        self.mc = MemexConfig()
        self.dbpath = self.mc.get(ConfigSection.DEFAULT, ConfigOption.DB_PATH)
        self.logfile = self.mc.get(ConfigSection.DEFAULT, ConfigOption.LOG_FILE)
        self.set_logging()

    def set_logging(self):
        logging.basicConfig(
            filename=self.logfile,
            level=logging.INFO,
            format="%(asctime)s: (%(levelname)s) %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
        )

    def create_session(self):
        self.engine = create_engine("sqlite:///" + self.dbpath, echo=False, future=True)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        # self.session.expire_on_commit = False  # HOPEFULLY THIS IS NOT A PROBLEM

    def execute_sql(self, sql):
        self.engine = create_engine("sqlite:///" + self.dbpath, echo=False, future=True)
        with self.engine.connect() as con:
            rs = con.execute(text(sql))
            return list(rs)
        return None
