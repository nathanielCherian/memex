from memex.auth import gen_token, get_all_tokens
from memex.api import start_server
from argparse import ArgumentParser, RawTextHelpFormatter
import sys 

def not_found(x):
    print('command not recognized.')
    print('see help.')

def createtoken(parsed_args):
    sub_args = parsed_args.args
    name = sub_args[0] if len(sub_args) > 0 else input('identifying name for token: ')
    token = gen_token(name)
    if token:
        print(f'Here is your token: {token}')
        print('This will only be shown once.')
    else:
        print('ERROR: try again')

def listtokens(parsed_args):
    sub_args = parsed_args.args
    tokens = get_all_tokens()
    tokenstrs = list(map(lambda token: str(token.id).ljust(3) + token.get_name().ljust(10) + str(token.last_accessed), 
                    tokens))
    tokenstrs.insert(0, 'ID'.ljust(3)+'Name'.ljust(10) + 'Last Accessed')
    print('\n'.join(tokenstrs))


def start(parsed_args):
    start_server()
    return

def revoke(parsed_args):
    raise Exception("Not implemented yet")
    return

createtoken.usage = 'create <token-name>'
listtokens.usage = 'list'
start.usage = 'start'
revoke.usage = 'revoke <entry-id>'

commands = {
    'create':createtoken,
    'list':listtokens,
    'start':start,
    'revoke':revoke
}



def parse_args(args):
    parser = ArgumentParser(
        description="memex API and authorization tokens",
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