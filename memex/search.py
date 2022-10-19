from ast import keyword
from enum import Enum
from lib2to3.pgen2.token import OP
import re

from datetime import datetime

from sqlalchemy import and_, or_

from memex.entry_manager import EntryManager
from memex.errors import BasicException, InvalidQueryException
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

class Operator(Enum):
    OR = '||'
    AND = '&&'

OPERATORS = {
    "||":Operator.OR,
    '&&':Operator.AND,
}

# class BaseExpression:
#     def __init__(self, exp):
#         self.exp = exp
    
class Node:
    
    left = None
    op = None
    right = None

    leaf = False # is this a leaf node 
    def __init__(self, exp):
        self.exp = exp
        self.strip()
        self.visit()
        

    def strip(self): # Will strip parenthesis from beginig and end of expression
        self.exp = self.exp.strip()
        for _ in self.exp:
            if self.exp[0] == '(' and self.exp[-1] == ')':
                self.exp = self.exp[1:-1]
                continue
            break
        return

    def visit(self):
        state = 0
        for i, char in enumerate(self.exp):
            if char == "(":
                state += 1
            elif char == ')':
                state -= 1

            if (state == 0) and (re.match("\|\||&&", self.exp[i+1:i+3])):
                p1 = self.exp[0:i+1]
                p2 = self.exp[i+1:i+3]
                p3 = self.exp[i+3:]
                self.left = Node(p1)
                self.op = OPERATORS.get(p2, None)
                self.right = Node(p3)
                return
        # If reachers here it is an expression node (leaf)
        # Need a regex here to validate user input
        self.leaf = True
        match = re.match("keywords|url|id", self.exp)
        if not match: raise InvalidQueryException("Invalid query string: column name not recognized")
        self.column = match.group()
        self.value =  self.exp[len(self.column):]
        if self.value[0] != "=": raise InvalidQueryException("Invalid query string.")
        self.value = self.value[1:]
        self.type = FIELDS[self.column][0]
        self.value = self.type(self.value) # Casting to right data type

    def rebuild(self):
        if self.leaf:
            return self.exp
        return f'({self.left.rebuild()}{self.op.value}{self.right.rebuild()})'

    def build(self):
        if self.leaf:
            if self.type == str:
                comp = "regexp"
            else:
                comp = "="
            return f'({self.column} {comp} {self.value})'
        if self.op == Operator.OR:
            return f'({self.left.build()} OR {self.right.build()})'
        return f'({self.left.build()} AND {self.right.build()})'

    def __str__(self):
        if self.leaf:
            return f'<{self.exp}>'        
        return f'[{self.left} {self.op} {self.right}]'
        


if __name__ == "__main__":
    # exp = '(keywords="asdas"||(id=0&&id=1))&&keywords="asd"'
    # n = Node(exp)
    # print(n.rebuild())
    # em = EntryManager()
    # e = em.query().filter(or_(EntryModel.keywords == "article,series", and_(EntryModel.keywords == "hi", EntryModel.url == "yo"))).all()
    # print(e)
    exp = '((keywords=".tory"||id=1)&&url="https://.+")'
    n = Node(exp)
    print(n.rebuild())
    em = EntryManager()
    q = n.build()
    print(q)
    rs = em.execute_sql(f"SELECT * FROM entries WHERE {q}")
    for row in rs:
        print(row)

class PowerSearch:
    def __init__(self):
        self.em = EntryManager()

    def FTSearch(self, term, fields=None):
        if not fields:
            entryAttribs = [FIELDS[f][1] for f in FIELDS.keys() if FIELDS[f][0] == str]
        entries = self.em.query().filter(FIELDS['keywords'][1].op('regexp')(term)).all()
        # entries = (
        #     self.em.query()
        #     .filter(or_(*[MA.contains(term) for MA in entryAttribs]))
        #     .all()
        # )
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
