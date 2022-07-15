from asyncio import constants
from enum import unique
from pkg_resources import require
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AuthModel(Base):
    __tablename__ = "auth"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    salt = Column(String(64), nullable=False, unique=True)

    def __init__(self, name, salt):
        self.name = name
        self.salt = salt

    def __repr__(self):
        return f'<{self.__tablename__} id={self.id} name={self.name} salt={self.salt[:5]}>'

    def get_name(self):
        return self.name

class EntryModel(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True)
    