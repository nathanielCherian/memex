from memex.entry import create_entry
from memex.main import create_session
import random
import os

dirname = os.path.dirname(__file__)
nouns_file = os.path.join(dirname, 'data/nouns.txt')
test_db = os.path.join(dirname, 'example.db')

def populate_entries(n):
    nouns = open(nouns_file, 'r').read().split('\n')[:100]
    session = create_session()
    entries = [create_entry(url='http://example.com', keywords=random.choices(nouns, k=3)) for _ in range(n)]
    session.bulk_save_objects(entries)
    session.commit()

def timeit(func, desc):
    return

if __name__ == '__main__':
    os.remove(test_db)
    populate_entries(1000)