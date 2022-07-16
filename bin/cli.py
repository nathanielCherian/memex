from memex.auth import add_auth_token, gen_token, get_all_tokens
from memex.entry import create_entry, list_entries, save_entry
from argparse import ArgumentParser, RawTextHelpFormatter


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
    tokens = get_all_tokens()
    tokenstrs = map(lambda token: f'{token.get_name()}', tokens)
    print('\n'.join(tokenstrs))

def file_(sub_args):
    url = sub_args[0] if len(sub_args) > 0 else input('URL of website to store: ')
    keywords = sub_args[1:] if len(sub_args) > 1 else input('Enter keywords (comma seperated): ').split(',')
    entry = create_entry(url=url, keywords=keywords)
    status = save_entry(entry)
    print("Saved entry successfully!") if status else print("Failed to save entry...")

def list_(x):
    entries = list_entries()
    print(entries)

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

def main():
    parser = ArgumentParser(description='memex clis',
                formatter_class=RawTextHelpFormatter,
                epilog='\n'.join(list(map(lambda c: commands[c].usage, commands.keys())))
            )
    parser.add_argument('command', metavar='command', type=str, nargs=1,
                        help='<command>')
    parser.add_argument('args', metavar='args', type=str, nargs='*',
                        help='<args>')

    args = parser.parse_args()

    command = args.command[0]
    sub_args = args.args

    commands.get(command, not_found)(sub_args)

    

# print(args) epilog='\n'.join(map(lambda c: commands[c].usage, commands.keys()))
