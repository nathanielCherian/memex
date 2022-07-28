from sqlalchemy import and_, or_

from memex.main import create_session
from memex.models import EntryModel


def search_keywords_or(keywords):
    return search_keywords(or_, keywords)


def search_keywords_and(keywords):
    return search_keywords(and_, keywords)


def search_keywords(func, keywords):
    try:
        session = create_session()
        e = (
            session.query(EntryModel)
            .filter(func(*[EntryModel.keywords.contains(k) for k in keywords]))
            .all()
        )
        return e
    except Exception as e:
        print("unable to search...", e)
    return []


def search_url(substr):
    try:
        session = create_session()
        e = session.query(EntryModel).filter(EntryModel.url.contains(substr)).all()
        return e
    except Exception as e:
        print("unable to search...", e)
