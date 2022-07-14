import sqlite3
from main import create_session
from model import AuthModel

def find_token(salt):
    try:
        session = create_session()
        res = session.query(AuthModel).filter(AuthModel.salt == salt).first()
        return res
    except Exception as e:
        print("failed to search for token...", e)
    return

def get_all_tokens():
    try:
        session = create_session()
        return session.query(AuthModel).all()
    except Exception as e:
        print("failed to get all tokens...", e)
    return []

def add_auth_token(name, salt):
    try:
        session = create_session()
        auth = AuthModel(name, salt)
        session.add(auth)
        session.commit()
    except Exception as e:
        print('failed to add new token')
        return False
    return True


if __name__ == '__main__':
    print("starting...")

    print(get_all_tokens())
    add_auth_token('test', 'test-salt')

    print("finished")