from datetime import datetime
from enum import Enum

from memex.models import EntryModel


def create_field(type, column, searchable):
    return {"type": type, "column": column, "searchable": searchable}


FIELDS = {
    "id": create_field(int, EntryModel.id, False),
    "url": create_field(str, EntryModel.url, True),
    "keywords": create_field(str, EntryModel.keywords, True),
}
# FIELDS = {
#     "id": [int, EntryModel.id],
#     "url": [str, EntryModel.url],
#     "keywords": [str, EntryModel.keywords],
#     "time_created": [datetime, EntryModel.time_created],
#     "time_updated": [datetime, EntryModel.time_updated],
# }


class Operator(Enum):
    OR = "||"
    AND = "&&"


OPERATORS = {
    "||": Operator.OR,
    "&&": Operator.AND,
}
