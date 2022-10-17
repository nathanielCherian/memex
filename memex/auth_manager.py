import hashlib
import logging
import uuid

from .errors import handle_error
from .main import create_session
from .models import AuthModel
from .session import BaseSession


class AuthManager(BaseSession):
    def gen_token(self, name):
        token = str(uuid.uuid4())
        salt = hashlib.sha256(str.encode(token)).hexdigest()
        status = self.add_auth_token(name, salt)
        return token

    def find_token(self, salt):
        try:
            self.create_session()
            res = self.session.query(AuthModel).filter(AuthModel.salt == salt).first()
            if res:
                res.touch()
                self.session.commit()
            return res
        except Exception as e:
            handle_error("Failed to find token.", e)

    def delete_token(self, id_):
        try:
            self.create_session()
            token = self.session.query(AuthModel).filter(AuthModel.id == id_).first()
            if not token:
                raise Exception("Token does not exist.")
            name = token.name
            salt = token.salt
            self.session.delete(token)
            self.session.commit()
        except Exception as e:
            handle_error("Unable to delete token.", e)
        return False

    def validate_token(self, token, bearer=""):
        salt = hashlib.sha256(str.encode(token)).hexdigest()
        search_res = self.find_token(salt)
        validity = True if search_res else False
        if validity:
            logging.info(
                f"Authenticated {bearer} with '{search_res.name}' ({search_res.salt[:5]})"
            )
        else:
            logging.warning(f"Failed to authenticate {bearer}")
        return validity

    def get_all_tokens(self):
        self.create_session()
        try:
            return self.session.query(AuthModel).all()
        except Exception as e:
            handle_error("Failed to retrieve tokens", e)
        return []

    def add_auth_token(self, name, salt):
        try:
            self.create_session()
            auth = AuthModel(name, salt)
            self.session.add(auth)
            self.session.commit()
            logging.info(f"Created new auth token '{name}' ({salt[:5]})")
        except Exception as e:
            handle_error("Failed to add new token.", e)
            return False
        return True
