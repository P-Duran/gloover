class WebPage(object):
    def __init__(self, company_name: str, domain: str, max_score: float):
        self.company_name = company_name
        self.domain = domain
        self.max_score = max_score
