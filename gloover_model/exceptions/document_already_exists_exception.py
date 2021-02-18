class DocumentAlreadyExistsException(Exception):
    def __init__(self, message, exception):
        self.exception = exception
        self.message = message
        super().__init__(self.message)

