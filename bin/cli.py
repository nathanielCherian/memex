from memex.auth import add_auth_token, gen_token, get_all_tokens
from memex.entry import create_entry, list_entries, save_entry
from argparse import ArgumentParser, RawTextHelpFormatter
import sys

def not_found(x):
    print('command not recognized.')
    print('see help.')

def createtoken(sub_args):
    name = sub_args[0] if len(sub_args) > 0 else input('identifying name for token: ')
    token = gen_token(name)
    if token:
        print(f'Here is your token: {token}')
        print('This will only be shown once.')
    else:
        print('ERROR: try again')


def listtokens(sub_args):
    name_pad = 10
    tokens = get_all_tokens()
    tokenstrs = list(map(lambda token: str(token.id).ljust(3) + token.get_name().ljust(10) + str(token.last_accessed), 
                    tokens))
    tokenstrs.insert(0, 'ID'.ljust(3)+'Name'.ljust(10) + 'Last Accessed')
    print('\n'.join(tokenstrs))

def file_(sub_args):
    url = sub_args[0] if len(sub_args) > 0 else input('URL of website to store: ')
    keywords = sub_args[1:] if len(sub_args) > 1 else input('Enter keywords (comma seperated): ').split(',')
    entry = create_entry(url=url, keywords=keywords)
    status = save_entry(entry)
    print("Saved entry successfully!") if status else print("Failed to save entry...")

def list_(x):
    entries = list_entries()
    r = lambda e: str(e.id).ljust(4) + e.url.ljust(19) + " "+str(e.keywords)
    entry_strs = list(map(r, entries))
    print('\n'.join(entry_strs))

def set_remote(x):
    raise Exception("not implemented yet.")

createtoken.usage = 'createtoken <token-name>'
listtokens.usage = 'listtokens'
file_.usage = 'file <url?> <keywords(csv)?>'
list_.usage = 'list'
set_remote.usage = 'set-remote <server-url>'


commands = {
    'createtoken':createtoken,
    'listtokens':listtokens,
    'file':file_,
    'list':list_,
    'set-remote':set_remote
}


def parse_args(args):
    parser = ArgumentParser(description='memex clis',
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
    sub_args = parsed_args.args
    commands.get(command, not_found)(sub_args)

    

def main():
    parsed_args = parse_args(sys.argv[1:])
    execute_args(parsed_args)

# print(args) epilog='\n'.join(map(lambda c: commands[c].usage, commands.keys()))
