# Functions related to displaying output to the end user
from .constants import FIELDS


def display_list(entries, columns=FIELDS.keys()):
    def formatter(entry):
        return ' '.join([str(entry[c]).ljust(FIELDS[c]["spacing"])[:FIELDS[c]["spacing"]] for c in columns])
    return list(map(formatter, entries))


def display_entry(entry):
    columns = ["url", "keywords", "time_created"]
    spacing = len(max(columns, key=len)) + 4
    return '\n'.join([c.ljust(spacing) + str(entry[c]) for c in columns])
