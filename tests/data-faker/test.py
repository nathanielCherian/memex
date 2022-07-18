from memex.entry import create_entry, save_entry
import random

def populate_entries(n):
    nouns = open('data/nouns.txt', 'r').read().split('\n')[:100]
    for i in range(n):
        entry = create_entry(url='http://example.com', keywords=random.choices(nouns, k=3))
        save_entry(entry)

if __name__ == '__main__':
    populate_entries(30)