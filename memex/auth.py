import hashlib
import logging
import uuid

from .errors import handle_error
from .main import create_session
from .models import AuthModel


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
        handle_error("Failed to find token", e)
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
        handle_error("Unable to delete token", e)
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
        logging.warning(f"Failed to authenticate {bearer}")
    return validity


def get_all_tokens():
    try:
        session = create_session()
        return session.query(AuthModel).all()
    except Exception as e:
        handle_error("Failed to retrieve tokens", e)
    return []


def add_auth_token(name, salt):
    try:
        session = create_session()
        auth = AuthModel(name, salt)
        session.add(auth)
        session.commit()

        logging.info(f"Created new auth token '{name}' ({salt[:5]})")
    except Exception as e:
        handle_error("Failed to add new token.", e)
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
        handle_error("Unable to revoke token", e)
