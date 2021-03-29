from datetime import datetime

from gloover_service.utils.logger import Logger


class Review(dict):
    def __init__(self, review_id: str, asin: str, text: str, author: str, date: datetime, country: str,
                 polarity: float, domain: str):
        self.review_id = review_id
        self.polarity = polarity
        self.country = country
        self.date = date
        self.text = text
        self.asin = asin
        self.author = author
        self.domain = domain
        dict.__init__(self, id=review_id, asin=asin, text=text, author=author, date=date,
                      country=country,
                      polarity=polarity, domain=domain)

    @classmethod
    def from_json(cls, json):
        try:
            json['date'] = datetime.strptime(json['date'], "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            Logger.log_warning(e)
        return cls(json['id'],
                   json['asin'],
                   json['text'],
                   json['author'],
                   json['date'],
                   json['country'],
                   json['polarity'],
                   json['domain'])

    def update_params(self, params: dict):
        self.__dict__.update(params)
        return self
