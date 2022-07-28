from memex.cli_handler import CLI, MemexCLI
from tests.utils import remove_db


def test_cli__list(capsys):
    MemexCLI(CLI.MEMEX, ["list"])


def test_cli__file(capsys):
    MemexCLI(CLI.MEMEX, ["file", "url", "keyword1", "keyword2", "keyword3"])


def test_cli__search(capsys):
    MemexCLI(CLI.MEMEX, ["search", "search_term1", "search_term2"])


def test_server__create(capsys):
    MemexCLI(CLI.MEMEX_API, ["create", "token_name"])


def test_server__list(capsys):
    MemexCLI(CLI.MEMEX_API, ["list"])


def test_server__revoke(capsys):
    MemexCLI(CLI.MEMEX_API, ["revoke", "1"])
