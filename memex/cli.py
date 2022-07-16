from database.auth import add_auth_token, get_all_tokens
from database.entry import create_entry, list_entries, save_entry
import argparse
import uuid
import hashlib


parser = argparse.ArgumentParser(description='memex clis')
parser.add_argument('command', metavar='command', type=str, nargs=1,
                    help='<command>')
parser.add_argument('args', metavar='args', type=str, nargs='*',
                    help='<args>')

args = parser.parse_args()

command = args.command[0]
sub_args = args.args

if command == 'addtoken':
    name = sub_args[0] if len(sub_args) > 0 else input('identifying name for token: ')
    token = str(uuid.uuid4())
    salt = hashlib.sha256(str.encode(token)).hexdigest()
    status = add_auth_token(name, salt)
    if status:
        print(f'Here is your token: {token}')
        print('This will only be shown once.')
    else:
        print('ERROR: try again')

elif command == 'listtokens':
    tokens = get_all_tokens()
    tokenstrs = map(lambda token: f'{token.get_name()}', tokens)
    print('\n'.join(tokenstrs))

elif command == 'file':
    url = sub_args[0] if len(sub_args) > 0 else input('URL of website to store: ')
    keywords = sub_args[1:] if len(sub_args) > 1 else input('Enter keywords (comma seperated): ').split(',')
    entry = create_entry(url=url, keywords=keywords)
    status = save_entry(entry)
    print("Saved entry successfully!") if status else print("Failed to save entry...")

elif command == 'list':
    entries = list_entries()
    print(entries)

elif command == 'set-remote':
    raise Exception("not implemented yet.")

else:
    print('command not recognized.')
    print('see help.')


# print(args)
