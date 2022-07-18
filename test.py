from memex.models import EntryModel
from memex.search import exec_command, search_keywords

exec_command("SELECT * from entries WHERE instr(keywords, 'government') > 0 OR instr(keywords, 'information') > 0;")

from memex.main import create_session


session = create_session()

# entries = session.query(EntryModel).filter(EntryModel.keywords.contains('government')).all()
# print(entries)

search_keywords(['government','information'])