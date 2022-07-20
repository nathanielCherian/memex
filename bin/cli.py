from memex.entry import create_entry, find_entry, list_entries, save_entry
from argparse import ArgumentParser, RawTextHelpFormatter
import sys

from memex.search import search_keywords_or

def not_found(x):
    print('command not recognized.')
    print('see help.')


def file_(parsed_args):
    sub_args = parsed_args.args
    url = sub_args[0] if len(sub_args) > 0 else input('URL of website to store: ')
    keywords = sub_args[1:] if len(sub_args) > 1 else input('Enter keywords (comma seperated): ').split(',')
    entry = create_entry(url=url, keywords=keywords)
    status = save_entry(entry)
    print("Saved entry successfully!") if status else print("Failed to save entry...")

def list_(x):
    entries = list_entries()
    print(f"showing {len(entries)} entries")
    r = lambda e: str(e.id).ljust(4) + e.url.ljust(19) + " "+str(e.keywords)
    entry_strs = list(map(r, entries))
    print('\n'.join(entry_strs))

def search(parsed_args):
    sub_args = parsed_args.args
    if len(sub_args) < 1:
        print('No search queries provided.')
        return
    entries = search_keywords_or(sub_args)
    print(f'Found {len(entries)} entries...')
    r = lambda e: str(e.id).ljust(4) + e.url.ljust(19) + " "+str(e.keywords)
    entry_strs = list(map(r, entries))
    print('\n'.join(entry_strs))
    

def inspect(parsed_args):
    sub_args = parsed_args.args
    entry = find_entry(sub_args[0])
    if entry is None: 
        print("That entry does not exist.")
        return
    print(f'url: {entry.url}\ndate-created: {entry.time_created}\nkeywords: {entry.keywords}\n')


def set_remote(x):
    raise Exception("not implemented yet.")

file_.usage = 'file <url?> <keywords (csv)?>'
list_.usage = 'list'
set_remote.usage = 'set-remote <server-url>'
search.usage = 'search [keywords...]'
inspect.usage = 'inspect <entry-id>'


commands = {
    'file':file_,
    'list':list_,
    'set-remote':set_remote,
    'search':search,
    'inspect':inspect,
}


def parse_args(args):
    parser = ArgumentParser(
        description='memex clis',
        formatter_class=RawTextHelpFormatter,
        epilog='\n'.join(list(map(lambda c: commands[c].usage, commands.keys())))
    )
    parser.add_argument('command', metavar='command', type=str, nargs=1,
                        help='<command>')
    parser.add_argument('args', metavar='args', type=str, nargs='*',
                        help='<args>')

    return parser.parse_args(args)

def execute_args(parsed_args):
    command = parsed_args.command[0]
    commands.get(command, not_found)(parsed_args)



def main(args=None):
    if args is None: args = sys.argv[1:]
    parsed_args = parse_args(args)
    execute_args(parsed_args)
