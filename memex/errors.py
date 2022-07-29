import logging


def handle_error(message, e):
    print(message, e)
    logging.error(message, e)


class InvalidKeywordException(Exception):
    pass


class BasicException(Exception):
    def __init__(self, message):
        super().__init__(message)
