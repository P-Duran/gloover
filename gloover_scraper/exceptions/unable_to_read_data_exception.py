class UnableToReadDataException(Exception):
    def __init__(self, e: Exception, msg: str):
        self.traceback = str(e)
        self.msg = msg