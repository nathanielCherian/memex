from asyncio import constants
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from constants import DB_PATH
from model import Base, AuthModel, EntryModel

engine = create_engine("sqlite:///"+DB_PATH, echo=True, future=True)
Base.metadata.create_all(engine)

session = Session(engine)

def get_auth_by_salt(salt):
    res = session.query(AuthModel).filter(AuthModel.salt == salt).first()
    return res

def get_all_auth():
    return session.query(AuthModel).all()

# auth = AuthModel("test-name", "test-salt")
# session.add(auth)
# session.commit()
# res = session.query(AuthModel).all()
# print(res)

print('LIST OF AUTH TOKENS: ', get_all_auth())

res = get_auth_by_salt('test-salt')
print('FOUND TOKEN: ', res)
