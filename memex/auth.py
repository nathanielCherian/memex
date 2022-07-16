from operator import truediv
from .main import create_session
from .models import AuthModel
import hashlib
import uuid

def gen_token(name):
    token = str(uuid.uuid4())
    salt = hashlib.sha256(str.encode(token)).hexdigest()
    status = add_auth_token(name, salt)
    return token

def find_token(salt):
    try:
        session = create_session()
        res = session.query(AuthModel).filter(AuthModel.salt == salt).first()
        return res
    except Exception as e:
        print("failed to search for token...", e)
    return None

def validate_token(token):
    salt = hashlib.sha256(str.encode(token)).hexdigest()
    search_res = find_token(salt)
    if search_res:
        return True
    return False

def get_all_tokens():
    try:
        session = create_session()
        return session.query(AuthModel).all()
    except Exception as e:
        print("failed to get tokens...", e)
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

