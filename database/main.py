from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from constants import DB_PATH
from model import Base 


def create_session():
    engine = create_engine("sqlite:///"+DB_PATH, echo=False, future=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    return session

