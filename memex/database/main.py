from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database.constants import DB_PATH
from database.models import Base 


def create_session():
    engine = create_engine("sqlite:///"+DB_PATH, echo=False, future=True)
    Base.metadata.create_all(engine)
    session = Session(engine)
    return session

