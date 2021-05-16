from .gloover_exception import GlooverException


class RequestArgsException(GlooverException):
    def __init__(self, msg: str):
        self.message = msg
