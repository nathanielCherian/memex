from .main import create_session
from .models import AuthModel
import hashlib
import uuid
import logging


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


def delete_token(id_):
    try:
        session = create_session()
        token = session.query(AuthModel).filter(AuthModel.id == id_).first()
        if not token:
            raise Exception("token does not exist")
        name = token.name
        salt = token.salt
        session.delete(token)
        session.commit()

        logging.info(f"Revoked auth token '{name}' ({salt[:5]})")
        return True
    except Exception as e:
        print("something went wrong...", e)
    return False


def validate_token(token, bearer=""):
    salt = hashlib.sha256(str.encode(token)).hexdigest()
    search_res = find_token(salt)
    validity = True if search_res else False
    if validity:
        logging.info(
            f"Authenticated {bearer} with '{search_res.name}' ({search_res.salt[:5]})"
        )
    else:
        logging.warn(f"Failed to authenticate {bearer}")
    return validity


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

        logging.info(f"Created new auth token '{name}' ({salt[:5]})")
    except Exception as e:
        print("failed to add new token", e)
        return False
    return True


def revoke_token(id_):
    try:
        session = create_session()
        res = session.query(AuthModel).filter(AuthModel.id == id_).first()
        if not res:
            raise Exception("Not found")
        session.commit()

        logging.info(f"Revoked auth token '{res.name}' ({res.salt[:5]})")

    except Exception as e:
        print("something went wrong revoking...", e)
