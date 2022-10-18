import logging


def handle_error(message, e, verbose=True):
    if verbose:
        print(message, e)
    logging.error(message, e)


class InvalidKeywordException(Exception):
    pass

class InvalidQueryException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BasicException(Exception):
    def __init__(self, message):
        super().__init__(message)
