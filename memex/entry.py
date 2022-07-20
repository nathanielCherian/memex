from .main import create_session
from .models import EntryModel
from .errors import InvalidKeywordException

def create_from_dict(dict):
    attribs = ['url', 'keywords']
    kwargs = {k:dict[k] for k in attribs}
    return create_entry(**kwargs)

def create_entry(**kwargs):
    try:
        return EntryModel(**kwargs)
    except InvalidKeywordException as e:
        print("invalid keywords")
    except Exception as e:
        print("something went wrong..", e)
    return None

def save_entry(entry):
    try:
        session = create_session()
        session.add(entry)
        session.commit()
        return True
    except Exception as e:
        print("something went wrong")
        return False

def list_entries():
    try:
        session = create_session()
        return session.query(EntryModel).all()
    except Exception as e:
        print("something went wrong...", e)

def find_entry(id_):
    try:
        session = create_session()
        return session.query(EntryModel).filter(EntryModel.id == id_).first()
    except Exception as e:
        print("something went wrong...", e)