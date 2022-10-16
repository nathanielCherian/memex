import os
import random

from memex.entry_manager import create_entry
from memex.main import create_session

dirname = os.path.dirname(__file__)
nouns_file = os.path.join(dirname, "data/nouns.txt")
test_db = os.path.join(dirname, "example.db")


def populate_entries(n):
    nouns = open(nouns_file, "r").read().split("\n")[:99]
    website = lambda: f"https://{random.choice(nouns)}.com/"
    session = create_session()
    entries = [
        create_entry({"url": website(), "keywords": random.choices(nouns, k=2)})
        for _ in range(n)
    ]
    session.bulk_save_objects(entries)
    session.commit()
