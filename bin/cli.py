import argparse
from pydoc import describe
from memex.entry import create_entry, find_entry, list_entries, save_entry
from argparse import ArgumentParser, RawTextHelpFormatter
import sys
import csv

from memex.search import search_keywords_and, search_keywords_or

class BaseCommand():
    def __init__(self, subparsers) -> None:
        self.register_parser(subparsers)
        self.create_parser()
    
    def register_parser(self, subparsers):
        self.parser = subparsers.add_parser(self.command,
            description=self.description
        )

    def create_parser(self):
        return

    def handle_command(self, parsed_args):
        return
    
class FileCommand(BaseCommand):
    command = 'file'
    description = 'file description'

    def create_parser(self):
        self.parser.add_argument('url', metavar='url', nargs='?')
        self.parser.add_argument('keywords', metavar='keywords', nargs='*')
        return
    
    def handle_command(self, parsed_args):
        url = parsed_args.url if parsed_args.url else input('URL of website to store: ')
        keywords = parsed_args.keywords if parsed_args.keywords else input('Enter keywords (comma seperated): ').split(',')
        entry = create_entry({'url':url, 'keywords':keywords})
        status = save_entry(entry)
        print("Saved entry successfully!") if status else print("Failed to save entry...")


class ListCommand(BaseCommand):
    command = 'list'
    description = 'list description'

    def handle_command(self, parsed_args):
        entries = list_entries()
        print(f"showing {len(entries)} entries")
        r = lambda e: str(e.id).ljust(4) + e.url.ljust(19) + " "+str(e.keywords)
        entry_strs = list(map(r, entries))
        print('\n'.join(entry_strs))
        return 

class SearchCommand(BaseCommand):
    command = 'search'
    description = 'search description'

    def create_parser(self):
        self.parser.add_argument('terms', metavar='terms', nargs='*')
        self.parser.add_argument('-i', dest='intersection', action='store_true', help='Find intersection of search queries')
        return

    def handle_command(self, parsed_args):
        terms = parsed_args.terms
        intersection = parsed_args.intersection
        print(intersection)
        if len(terms) < 1:
            print('No search queries provided.')
            return

        entries = search_keywords_and(terms) if intersection else search_keywords_or(terms)

        print(f'Found {len(entries)} entries...')
        r = lambda e: str(e.id).ljust(4) + e.url.ljust(19) + " "+str(e.keywords)
        entry_strs = list(map(r, entries))
        print('\n'.join(entry_strs))
        return 

class InspectCommand(BaseCommand):
    command = 'inspect'
    description = 'inspect description'

    def create_parser(self):
        self.parser.add_argument('id', metavar='id', nargs=1, type=int)
    
    def handle_command(self, parsed_args):
        id_ = parsed_args.id[0]
        entry = find_entry(id_)
        if entry is None: 
            print("That entry does not exist.")
            return
        print(f'url: {entry.url}\ndate-created: {entry.time_created}\nkeywords: {entry.keywords}\n')

class ExportCommand(BaseCommand):
    command = 'export'
    description = 'export command'

    def handle_command(self, parsed_args):
        entries = list_entries()
        es = map(lambda e: e.to_csv(), entries)
        print('\n'.join(es))

# file_.usage = 'file <url?> <keywords?>', 'Stores a new entry to the database. keywords are space-seperated.'
# list_.usage = 'list', 'Shows all entrys in the database'
# search.usage = 'search [keywords...]', 'Returns entries that match one or more of the keywords given. Keywords are space-seperated'
# inspect.usage = 'inspect <entry-id>', 'Displays full entry of given id.'
# export.usage = 'export', 'prints the database to output in CSV format'
# set_remote.usage = 'set-remote <server-url>'

def parse_args(args):

    # epilog = '\n'.join(
    #     list(map(
    #         lambda c: commands[c].usage[0].ljust(30)+commands[c].usage[1],
    #         commands.keys()
    #     ))
    # )

    parser = ArgumentParser(
        description='memex clis',
        formatter_class=RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(description='sub-description', dest='command')

    parsers = [
        Command(subparsers)
        for Command in BaseCommand.__subclasses__()
    ]

    parsed_args = parser.parse_args(args)
    command = parsed_args.command

    for parser in parsers:
        if parser.command == command:
            parser.handle_command(parsed_args)
            return
    
    print()

    return

def main(args=None):
    if args is None: args = sys.argv[1:]
    parse_args(args)
