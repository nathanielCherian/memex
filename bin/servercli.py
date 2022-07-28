from pydoc import describe
from memex.auth import delete_token, gen_token, get_all_tokens
from memex.api import start_server
from argparse import ArgumentParser, RawTextHelpFormatter
import sys 

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

class CreateTokenCommand(BaseCommand):
    command = 'create'
    description = 'create token description'

    def create_parser(self):
        self.parser.add_argument('name', metavar='name', nargs='?')
        return
    
    def handle_command(self, parsed_args):
        name = parsed_args.name
        name = name if name else input('identifying name for token: ')
        token = gen_token(name)
        if token:
            print(f'Here is your token: {token}')
            print('This will only be shown once.')
        else:
            print('ERROR: try again')

class ListTokenCommand(BaseCommand):
    command = 'list'
    description = 'list tokens description'

    def handle_command(self, parsed_args):
        tokens = get_all_tokens()
        tokenstrs = list(map(lambda token: str(token.id).ljust(3) + token.get_name().ljust(10) + str(token.last_accessed), 
                        tokens))
        tokenstrs.insert(0, 'ID'.ljust(3)+'Name'.ljust(10) + 'Last Accessed')
        print('\n'.join(tokenstrs))

class RevokeTokenCommand(BaseCommand):
    command = 'revoke'
    description = 'revoke token command'

    def create_parser(self):
        self.parser.add_argument('id', metavar='id', nargs=1, type=int)
        return
    
    def handle_command(self, parsed_args):
        id_ = parsed_args.id[0]
        status = delete_token(id_)
        if status: print("Successfully revoked token.")

class StartAPICommand(BaseCommand):
    command = 'start'
    description = 'start api command'

    def handle_command(self, parsed_args):
        start_server()


# createtoken.usage = 'create <token-name>'
# listtokens.usage = 'list'
# start.usage = 'start'
# revoke.usage = 'revoke <token-id>'

# commands = {
#     'create':createtoken,
#     'list':listtokens,
#     'start':start,
#     'revoke':revoke
# }


def parse_args(args):

    parser = ArgumentParser(
        description='memex API and token authorization',
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