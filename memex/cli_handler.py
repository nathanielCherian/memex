import sys
from argparse import ArgumentParser
from enum import Enum

from memex.models import EntryModel
from memex.remote import MemexRemote

from . import __version__
from .api import start_server
from .auth import delete_token, gen_token, get_all_tokens
from .config import ConfigOption, ConfigSection, MemexConfig
from .entry import (EntryManager, create_entry, find_entry, list_entries,
                    save_entry)
from .search import PowerSearch


class CLI(Enum):
    MEMEX = 1
    MEMEX_API = 2


class BaseCommand:
    def __init__(self, subparsers) -> None:
        self.register_parser(subparsers)
        self.create_parser()

    def register_parser(self, subparsers):
        self.parser = subparsers.add_parser(self.command, description=self.description)

    def create_parser(self):
        return

    def get_args(self, parsed_args):
        return {}

    def display(self, model):
        return

    def handle_command(self, parsed_args):
        return

    @staticmethod
    def match(command):
        return


class MemexCommand(BaseCommand):
    def __init__(self, subparsers) -> None:
        super().__init__(subparsers)
        self.entry_manager = EntryManager()


class MemexAPICommand(BaseCommand):
    pass


def remote(func):
    mc = MemexConfig()
    remote_url = mc.get(ConfigSection.DEFAULT, ConfigOption.REMOTE)

    def remote_runner(*args, **kwargs):
        command_obj = args[0]
        command = command_obj.command

        print(f"Executing '{command}' on remote server {remote_url}")

        parsed_args = args[1]
        command_args = command_obj.get_args(parsed_args)
        token = mc.get(ConfigSection.DEFAULT, ConfigOption.TOKEN)

        mr = MemexRemote(remote_url, token)
        json_res = mr.execute(command, command_args)
        command_obj.display(json_res)

    if remote_url:
        return remote_runner
    return func


# commands for MEMEX


class FileCommand(MemexCommand):
    command = "file"
    description = "Stores a new entry to the database. keywords are space-seperated."

    def create_parser(self):
        self.parser.add_argument("url", metavar="url", nargs="?")
        self.parser.add_argument("keywords", metavar="keywords", nargs="*")
        return

    def get_args(self, parsed_args):
        url = parsed_args.url if parsed_args.url else input("URL of website to store: ")
        keywords = (
            parsed_args.keywords
            if parsed_args.keywords
            else input("Enter keywords (comma seperated): ").split(",")
        )
        return {"url": url, "keywords": keywords}

    def display(self, model):
        print("Saved entry successfully!") if model else print(
            "Failed to save entry..."
        )
        return

    @remote
    def handle_command(self, parsed_args):
        args = self.get_args(parsed_args)
        entry = create_entry({"url": args["url"], "keywords": args["keywords"]})
        status = save_entry(entry)
        self.display


class ListCommand(MemexCommand):
    command = "list"
    description = "Shows all entries in the database"

    def display(self, model):
        entries = model["entries"]
        print(f"showing {len(entries)} entries")
        r = (
            lambda e: str(e["id"]).ljust(4)
            + e["url"].ljust(19)
            + " "
            + str(e["keywords"])
        )
        entry_strs = list(map(r, entries))
        print("\n".join(entry_strs))
        return

    @remote
    def handle_command(self, parsed_args):
        entries = self.entry_manager.list_entries()
        self.display({"entries": [entry.as_dict() for entry in entries]})
        return


class SearchCommand(MemexCommand):
    command = "search"
    description = "Returns entries that match one or more of the keywords given. Keywords are space-seperated"

    def create_parser(self):
        self.parser.add_argument("terms", metavar="terms", nargs="*")
        group = self.parser.add_mutually_exclusive_group(required=False)
        group.add_argument(
            "-i",
            "--intersection",
            dest="intersection",
            const="and",
            nargs="?",
            help="Find intersection of search terms",
        )

        group.add_argument(
            "-u",
            "--union",
            dest="intersection",
            const="or",
            nargs="?",
            help="Find union of search terms",
        )
        return

    def get_args(self, parsed_args):
        terms = parsed_args.terms
        if len(terms) < 1:
            print("No search queries provided.")
            exit()
        return {
            "terms": terms,
            "operation": parsed_args.intersection,
            "fields": ["keywords"],
        }

    def display(self, model):
        entries = model["entries"]
        print(f"found {len(entries)} entries")
        r = (
            lambda e: str(e["id"]).ljust(4)
            + e["url"].ljust(19)
            + " "
            + str(e["keywords"])
        )
        entry_strs = list(map(r, entries))
        print("\n".join(entry_strs))
        return

    @remote
    def handle_command(self, parsed_args):
        args = self.get_args(parsed_args)
        terms = args["terms"]
        operation = args["operation"]
        fields = args["fields"]

        entries = PowerSearch(terms, operation, fields).execute()

        self.display({"entries": [entry.as_dict() for entry in entries]})
        return


class InspectCommand(MemexCommand):
    command = "inspect"
    description = "Displays full entry of given id."

    def create_parser(self):
        self.parser.add_argument("id", metavar="id", nargs=1, type=int)

    def get_args(self, parsed_args):
        return {"id": parsed_args.id[0]}

    def display(self, model):
        entry = model["entry"]
        if entry is None:
            print("That entry does not exist.")
            return
        print(
            f"url: {entry['url']}\ndate-created: {entry['time_created']}\nkeywords: {entry['keywords']}\n"
        )
        return

    @remote
    def handle_command(self, parsed_args):
        id_ = self.get_args(parsed_args)["id"]
        entry = self.entry_manager.find_entry(id_)
        self.display({"entry": entry.as_dict()})


class ExportCommand(MemexCommand):
    command = "export"
    description = "exports all entries to csv format"

    def display(self, model):
        entries = model["entries"]
        es = map(lambda e: EntryModel.dict_csv(e), entries)
        print("\n".join(es))
        return

    @remote
    def handle_command(self, parsed_args):
        entries = self.entry_manager.list_entries()
        self.display({"entries": [entry.as_dict() for entry in entries]})


class SetRemoteCommand(MemexCommand):
    command = "set-remote"
    description = "set remote memex API endpoint. Leave blank to turn off"

    def create_parser(self):
        self.parser.add_argument(
            "endpoint", metavar="endpoint", nargs="?", default="", type=str
        )

    def handle_command(self, parsed_args):
        endpoint = parsed_args.endpoint
        token = ""
        if endpoint == "":
            print("Removed API remote, switched to local storage.")
        else:
            token = input("token: ").strip()
            print(f"Switched API remote to {endpoint}.")

        mc = MemexConfig()
        mc.set(ConfigSection.DEFAULT, ConfigOption.REMOTE, endpoint)
        mc.set(ConfigSection.DEFAULT, ConfigOption.TOKEN, token)

        print("Try running 'memex list' to test new storage option")


# Commands for MEMEX API
class CreateTokenCommand(MemexAPICommand):
    command = "create"
    description = "creates a new authorization token"

    def create_parser(self):
        self.parser.add_argument("name", metavar="name", nargs="?")
        return

    def handle_command(self, parsed_args):
        name = parsed_args.name
        name = name if name else input("identifying name for token: ")
        token = gen_token(name)
        if token:
            print(f"Here is your token: {token}")
            print("This will only be shown once.")
        else:
            print("ERROR: try again")


class ListTokenCommand(MemexAPICommand):
    command = "list"
    description = "lists all valid tokens"

    def handle_command(self, parsed_args):
        tokens = get_all_tokens()
        tokenstrs = list(
            map(
                lambda token: str(token.id).ljust(3)
                + token.get_name().ljust(10)
                + str(token.last_accessed),
                tokens,
            )
        )
        tokenstrs.insert(0, "ID".ljust(3) + "Name".ljust(10) + "Last Accessed")
        print("\n".join(tokenstrs))


class RevokeTokenCommand(MemexAPICommand):
    command = "revoke"
    description = "revokes a token using its id"

    def create_parser(self):
        self.parser.add_argument("id", metavar="id", nargs=1, type=int)
        return

    def handle_command(self, parsed_args):
        id_ = parsed_args.id[0]
        status = delete_token(id_)
        if status:
            print("Successfully revoked token.")


class StartAPICommand(MemexAPICommand):
    command = "start"
    description = "starts the API"

    def handle_command(self, parsed_args):
        start_server()


# Final memex cli class


class MemexCLI:
    def __init__(self, cli, args=[]) -> None:
        if not args:
            args = sys.argv[1:]

        description = (
            "memex cli to interact with your database"
            if cli == CLI.MEMEX
            else "memex API and token authorization"
        )
        parser = ArgumentParser(description=description)

        parser.add_argument("-v", "--version", action="version", version=__version__)
        subparsers = parser.add_subparsers(
            description="sub-description", dest="command"
        )

        CLICommand = MemexCommand if cli == CLI.MEMEX else MemexAPICommand

        Commands = CLICommand.__subclasses__()
        parsers = [Command(subparsers) for Command in Commands]

        parsed_args = parser.parse_args(args)
        command = parsed_args.command

        for parser in parsers:
            if parser.command == command:
                parser.handle_command(parsed_args)
                return

        print(description + "\n")
        for Command in CLICommand.__subclasses__():
            print(Command.command.ljust(20) + Command.description)
        print("\nuse the '-h' flag after each command to see usage")
