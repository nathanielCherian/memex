from bin.memex import main as cli_main
from bin.memex_api import main as server_main
from tests.utils import remove_db


def test_cli__list(capsys):
    cli_main(["list"])


def test_cli__file(capsys):
    cli_main(["file", "url", "keyword1", "keyword2", "keyword3"])


def test_cli__search(capsys):
    cli_main(["search", "search_term1", "search_term2"])


def test_server__create(capsys):
    server_main(["create", "token_name"])


def test_server__list(capsys):
    server_main(["list"])


def test_server__revoke(capsys):
    server_main(["revoke", "1"])
