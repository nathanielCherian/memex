from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from memex.config import read_config
from .models import Base 


def create_session():
    conf = read_config()
    dbpath = conf['DEFAULT']['db_path']
    engine = create_engine("sqlite:///"+dbpath, echo=False, future=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    session.expire_on_commit = False # HOPEFULLY THIS IS NOT A PROBLEM
    return session

def exec_command(command):
    engine = create_engine("sqlite:///example.db")
    with engine.connect() as con:
        rs = con.execute(command)
        return list(rs)