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
        if res:
            res.touch()
            session.commit()
        return res
    except Exception as e:
        print("failed to search for token...", e)
    return None

def validate_token(token):
    salt = hashlib.sha256(str.encode(token)).hexdigest()
    search_res = find_token(salt)
    validity = True if search_res is not None and search_res.valid else False
    return validity

def get_all_tokens():
    try:
        session = create_session()
        return session.query(AuthModel).filter(AuthModel.valid == True).all()
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
        print('failed to add new token', e)
        return False
    return True

def revoke_token(id_):
    try:
        session = create_session()
        res = session.query(AuthModel).filter(AuthModel.id == id_).first()
        if not res: return
        res.valid = False
        session.commit()
    except Exception as e:
        print("something went wrong revoking...",e)
        