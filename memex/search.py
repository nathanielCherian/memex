from datetime import datetime

from sqlalchemy import and_, or_

from memex.entry_manager import EntryManager
from memex.models import EntryModel

# My vision for PowerSearch
# - Full text search
# - provide a list of columns to run full text search one

FIELDS = {
    "id": [int, EntryModel.id],
    "url": [str, EntryModel.url],
    "keywords": [str, EntryModel.keywords],
    "time_created": [datetime, EntryModel.time_created],
    "time_updated": [datetime, EntryModel.time_updated],
}


class PowerSearch:
    def __init__(self):
        self.em = EntryManager()

    def FTSearch(self, term, fields=None):
        if not fields:
            entryAttribs = [FIELDS[f][1] for f in FIELDS.keys() if FIELDS[f][0] == str]
        entries = (
            self.em.query()
            .filter(or_(*[MA.contains(term) for MA in entryAttribs]))
            .all()
        )
        return entries


if __name__ == "__main__":
    entries = PowerSearch().FTSearch("story")
    print(entries)

# class PowerSearch:
#     # Extend PowerSearch in the future, it will be the selling point of memex
#     # Fast, Simple, Powerful
#     # Eventually, I might move away from the ORM and have the SQL builder be here
#     # ^ but maybe not

#     def __init__(self, terms, operation="or", fields=["keywords"]):
#         self.terms = terms
#         self.operation = operation
#         self.fields = fields

#     def execute(self):
#         op_func = or_ if self.operation == "or" else and_
#         # session = create_session()
#         entries = []
#         for field in self.fields:
#             ModelAttrib = None
#             if field == "keywords":
#                 ModelAttrib = EntryModel.keywords
#             if field == "url":
#                 ModelAttrib = EntryModel.url

#             e = (
#                 session.query(EntryModel)
#                 .filter(op_func(*[ModelAttrib.contains(t) for t in self.terms]))
#                 .all()
#             )
#             entries += e
#         return entries


# def search_keywords_or(keywords):
#     return search_keywords(or_, keywords)


# def search_keywords_and(keywords):
#     return search_keywords(and_, keywords)


# def search_keywords(func, keywords):
#     try:
#         session = create_session()
#         e = (
#             session.query(EntryModel)
#             .filter(func(*[EntryModel.keywords.contains(k) for k in keywords]))
#             .all()
#         )
#         return e
#     except Exception as e:
#         print("unable to search...", e)
#     return []


# def search_url(substr):
#     try:
#         session = create_session()
#         e = session.query(EntryModel).filter(EntryModel.url.contains(substr)).all()
#         return e
#     except Exception as e:
#         print("unable to search...", e)
