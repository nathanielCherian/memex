from email.policy import default
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from datetime import datetime
from .errors import InvalidKeywordException

Base = declarative_base()

class AuthModel(Base):
    __tablename__ = "auth"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    salt = Column(String(64), nullable=False, unique=True)
    last_accessed = Column(DateTime(timezone=True), default=None)
    valid = Column(Boolean(), default=True)

    def __init__(self, name, salt):
        self.name = name
        self.salt = salt

    def __repr__(self):
        return f'<{self.__tablename__} id={self.id} name={self.name} salt={self.salt[:5]}>'

    def get_name(self):
        return self.name

    def touch(self):
        self.last_accessed = datetime.now()


class EntryModel(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(200), nullable=False)
    keywords = Column(String(200))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __init__(self, url, keywords):
        self.url = url
        if type(keywords) == str:
            keywords = keywords.split(',')
        if ','.join(keywords).split(',') != keywords: raise InvalidKeywordException()
        self.keywords = ','.join(keywords)
    
    def __repr__(self):
        return f'<Entry id={self.id} url={self.url[:5]} keywords={self.keywords} time_created={self.time_created} time_updated={self.time_updated}>'
    
    @staticmethod
    def csv_headers():
        return 'id, url, keywords, time_created, time_updated'

    def to_csv(self):
        return f'{self.id}, "{self.url}", "{self.keywords}", "{self.time_created}", {self.time_updated}'

    def as_dict(self):
        l = ['id', 'url', 'keywords']
        return {k:self.__dict__[k] for k in l}

