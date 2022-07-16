from database.main import create_session
from database.models import EntryModel
from database.errors import InvalidKeywordException

def create_entry(**kwargs):
    try:
        return EntryModel(**kwargs)
    except InvalidKeywordException as e:
        print("invalid keywords")
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