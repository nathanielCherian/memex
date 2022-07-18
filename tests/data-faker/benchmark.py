from memex.entry import create_entry
from memex.main import create_session
import random
import time
import os

from memex.search import search_keywords, search_keywords_and, search_keywords_or

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
    start = time.perf_counter()
    out = func()
    end = time.perf_counter()
    print("elapsed time for '"+desc+ "' "+str(end-start))
    return out

if __name__ == '__main__':
    os.remove(test_db)
    timeit(lambda: populate_entries(10000), "database population")
    _ = timeit(lambda: search_keywords_or(['government']), "one word search")
    _ = timeit(lambda: search_keywords_or(['government', 'instruction']), "two word search")
    _ = timeit(lambda: search_keywords_and(['government', 'instruction']), "two word intersection search")

    # print('\n'.join([str(e) for e in entries]))
    # populate_entries(1000)
