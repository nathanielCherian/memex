from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .constants import DB_PATH
from .models import Base 


def create_session():
    engine = create_engine("sqlite:///"+DB_PATH, echo=False, future=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    session.expire_on_commit = False # HOPEFULLY THIS IS NOT A PROBLEM
    return session

