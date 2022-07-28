from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from memex.config import read_config
from .models import Base

import logging


def create_session():
    # READ CONF
    conf = read_config()
    dbpath = conf["DEFAULT"]["db_path"]

    # Create logger
    log_file = conf["DEFAULT"]["log_file"]
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s: (%(levelname)s) %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S",
    )

    engine = create_engine("sqlite:///" + dbpath, echo=False, future=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    session.expire_on_commit = False  # HOPEFULLY THIS IS NOT A PROBLEM
    return session


def exec_command(command):
    engine = create_engine("sqlite:///example.db")
    with engine.connect() as con:
        rs = con.execute(command)
        return list(rs)
