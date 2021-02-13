class WebPage(object):
    def __init__(self, name: str, url: str, max_score: float):
        self.name = name
        self.url = url
        self.max_score = max_score
