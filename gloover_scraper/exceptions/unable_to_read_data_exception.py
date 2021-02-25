from .gloover_scraper_exception import GlooverScraperException

class UnableToReadDataException(GlooverScraperException):
    def __init__(self, e: Exception, msg: str):
        self.traceback = str(e)
        self.message = msg