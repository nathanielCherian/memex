from memex.cli_handler import MemexCLI, CLI


def main():
    MemexCLI(CLI.MEMEX)


# # file_.usage = 'file <url?> <keywords?>', 'Stores a new entry to the database. keywords are space-seperated.'
# # list_.usage = 'list', 'Shows all entrys in the database'
# # search.usage = 'search [keywords...]', 'Returns entries that match one or more of the keywords given. Keywords are space-seperated'
# # inspect.usage = 'inspect <entry-id>', 'Displays full entry of given id.'
# # export.usage = 'export', 'prints the database to output in CSV format'
# # set_remote.usage = 'set-remote <server-url>'


#     print("Use the memex cli to interact with your database...\n")
#     for Command in BaseCommand.__subclasses__():
#         print(Command.command.ljust(20) + Command.description)
