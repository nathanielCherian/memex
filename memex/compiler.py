import re
from abc import abstractmethod

from memex.constants import FIELDS, OPERATORS, Operator
from memex.entry_manager import EntryManager
from memex.errors import InvalidQueryException


class Node:
    def __init__(self, exp):
        self.exp = exp
        self.strip()
        self.visit()

    def strip(self):  # Will strip parenthesis from beginig and end of expression
        self.exp = self.exp.strip()
        for _ in self.exp:
            if self.exp[0] == "(" and self.exp[-1] == ")":
                self.exp = self.exp[1:-1]
                continue
            break
        return

    @abstractmethod
    def visit(self):
        pass

    @abstractmethod
    def rebuild(self):
        pass

    @abstractmethod
    def build(self):
        pass


class LeafNode(Node):
    def visit(self):
        column_match = re.match("keywords|url|id", self.exp)
        if not column_match:
            raise InvalidQueryException(
                "Invalid query string: column name not recognized"
            )
        self.column = column_match.group() # grabbing column name
        self.type = FIELDS[self.column][0]

        self.value = self.exp[len(self.column):].strip() # getting the rest of the string

        # Finding the comparison
        comp_match = re.match("^(<=?|>=?)|=", self.value)
        if not comp_match:
            raise InvalidQueryException(
                "Invalid query string: invalid comparison"
            )
        self.comp = comp_match.group()
        self.value = self.value[len(self.comp):].strip() # What is left is the right hand side

        if self.type == str: # Making sure the right comparators are used
            if self.comp != '=':
                raise InvalidQueryException("Invalid query string: Can only use '=' on string columns")
            self.comp = "regexp"
        elif self.type == int:
            pass


        try: # Converting the right hand value into the type of the column
            self.value = self.type(self.value)  # Casting to right data type
        except Exception as e:
            raise InvalidQueryException("Invalid Query: Unable to parse argument, check that column and data types match")
 
    def rebuild(self):
        return self.exp

    def build(self):
        return f"({self.column} {self.comp} {self.value})"

    def __str__(self):
        return f"<{self.exp}>"


class BranchNode(Node):

    left = None
    op = None
    right = None

    leaf = False  # is this a leafode

    def visit(self):
        state = 0
        for i, char in enumerate(self.exp):
            if char == "(":
                state += 1
            elif char == ")":
                state -= 1

            if (state == 0) and (re.match("\|\||&&", self.exp[i + 1 : i + 3])):
                p1 = self.exp[0 : i + 1]
                p2 = self.exp[i + 1 : i + 3]
                p3 = self.exp[i + 3 :]
                self.left = BranchNode(p1)
                self.op = OPERATORS.get(p2, None)
                self.right = BranchNode(p3)
                return
        # If reachers here it is an expression node (leaf)
        self.leaf = LeafNode(self.exp)

    def rebuild(self):
        if self.leaf:
            return self.leaf.rebuild()
        return f"({self.left.rebuild()}{self.op.value}{self.right.rebuild()})"

    def build(self):
        if self.leaf:
            return self.leaf.build()
        if self.op == Operator.OR:
            return f"({self.left.build()} OR {self.right.build()})"
        return f"({self.left.build()} AND {self.right.build()})"

    def __str__(self):
        if self.leaf:
            return self.leaf.__str__()
        return f"[{self.left} {self.op} {self.right}]"


class Compiler:
    def __init__(self, exp) -> None:
        self.exp = exp
        self.head = BranchNode(exp)

    def to_sql(self):
        return self.head.build()

    def rebuild_query(self):
        return self.head.rebuild()


if __name__ == "__main__":

    def tester(exp):
        compiler = Compiler(exp)
        sql = compiler.to_sql()
        print(sql)

    exp = '((keywords=".tory"||id=1)&&url="https://.+")'
    # tester(exp)
    # tester('notright="test"')
    tester("id<=1")


    # Code below does what Compiler does
    # n = BranchNode(exp)
    # print(n.rebuild())
    # em = EntryManager()
    # q = n.build()
    # print(q)
    # rs = em.execute_sql(f"SELECT * FROM entries WHERE {q}")
    # for row in rs:
    #     print(row)
