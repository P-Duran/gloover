from .gloover_scraper_exception import GlooverScraperException


class NullRequestArgsException(GlooverScraperException):
    def __init__(self, msg: str):
        self.message = msg
