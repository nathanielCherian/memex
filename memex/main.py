# THIS FILE IS DEPRECATED
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from memex.config import ConfigOption, ConfigSection, MemexConfig

from .models import Base


def create_session():
    # READ CONF

    mc = MemexConfig()
    dbpath = mc.get(ConfigSection.DEFAULT, ConfigOption.DB_PATH)

    # Create logger
    log_file = mc.get(ConfigSection.DEFAULT, ConfigOption.LOG_FILE)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s: (%(levelname)s) %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S",
    )

    engine = create_engine("sqlite:///" + dbpath, echo=False, future=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    session.expire_on_commit = False  # HOPEFULLY THIS IS NOT A PROBLEM
    return session


# def exec_command(command):
#     engine = create_engine("sqlite:///example.db")
#     with engine.connect() as con:
#         rs = con.execute(command)
#         return list(rs)
