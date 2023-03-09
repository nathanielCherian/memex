from abc import abstractmethod

from memex.compiler import Compiler
from memex.constants import FIELDS
from memex.entry_manager import EntryManager

# My vision for PowerSearch
# - Full text search
# - provide a list of columns to run full text search one


class PowerSearch:
    def __init__(self):
        self.em = EntryManager()

    def FTSearch(self, term, fields=None):
        # if not fields:
        #     entryAttribs = [FIELDS[f][1] for f in FIELDS.keys() if FIELDS[f][0] == str]
        entries = (
            self.em.query()
            .filter(FIELDS["keywords"]["column"].op("regexp")(term))
            .all()
        )
        return entries

    def query_seach(self, query, rebuild=False):
        compiler = Compiler(query)
        sql_search = compiler.to_sql()
        rs = self.em.execute_sql(f"SELECT * FROM entries WHERE {sql_search}")
        columns = FIELDS.keys()
        entries = [{column: r[i] for i, column in enumerate(columns)} for r in rs]
        if rebuild:
            return (
                entries,
                compiler.rebuild_query()[1:-1],
            )  # [-1:-1] to cut off extra parenthesis
        return entries

    # def faceted_search(self, query):


# if __name__ == "__main__":
#     entries = PowerSearch().FTSearch("story")
#     print(entries)

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
