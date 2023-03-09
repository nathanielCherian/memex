from datetime import datetime
from enum import Enum

from memex.models import EntryModel


# type: python type of the column
# column: column name from models.EntryModel
# searchable: Can this column be searched directly (is it a string)
# spacing: When displaying, how many characters might this be
def create_field(type, column, searchable, spacing):
    return {"type": type, "column": column, "searchable": searchable, "spacing":spacing}


FIELDS = {
    "id": create_field(int, EntryModel.id, False, 4),
    "url": create_field(str, EntryModel.url, True, 20),
    "keywords": create_field(str, EntryModel.keywords, True, 20),
    "time_created":create_field(datetime, EntryModel.time_created, False, 10)
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
