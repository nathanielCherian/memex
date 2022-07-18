from sqlalchemy import or_
from memex.main import create_session
from memex.models import EntryModel

def search_keywords(keywords):
    try:
        session = create_session()
        e = session.query(EntryModel).filter(or_(*[EntryModel.keywords.contains(k) for k in keywords])).all()
        return e
    except Exception as e:
        print("unable to search...", e)
    return []


# def search_keywords(keyword):
