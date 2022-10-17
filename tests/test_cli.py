from memex.cli_handler import CLI, MemexCLI


def test_cli__list():
    MemexCLI(CLI.MEMEX, ["list"])


def test_cli__file():
    MemexCLI(CLI.MEMEX, ["file", "url", "keyword1", "keyword2", "keyword3"])


# def test_cli__search():
#    MemexCLI(CLI.MEMEX, ["search", "search_term1", "search_term2"])


def test_server__create():
    MemexCLI(CLI.MEMEX_API, ["create", "token_name"])


def test_server__list():
    MemexCLI(CLI.MEMEX_API, ["list"])


def test_server__revoke():
    MemexCLI(CLI.MEMEX_API, ["revoke", "1"])
