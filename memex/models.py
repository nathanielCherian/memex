from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

from .errors import InvalidKeywordException

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
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200), nullable=False)
    keywords = Column(String(200))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __init__(self, url, keywords):
        self.url = url
        if ','.join(keywords).split(',') != keywords: raise InvalidKeywordException()
        self.keywords = ','.join(keywords)
    
    def __repr__(self):
        return f'<Entry id={self.id} url={self.url[:5]} keywords={self.keywords} time_created={self.time_created} time_updated={self.time_updated}>'