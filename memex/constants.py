from enum import Enum
from memex.models import EntryModel
from datetime import datetime

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
