from .gloover_exception import GlooverException


class NullRequestArgsException(GlooverException):
    def __init__(self, msg: str):
        self.message = msg
