import uuid
from datetime import datetime


class Review(dict):
    def __init__(self, review_id: str, product_name: str, text: str, author: str, date: datetime, country: str,
                 polarity: float, domain: str):
        self.review_id = review_id
        self.polarity = polarity
        self.country = country
        self.date = date
        self.text = text
        self.product_name = product_name
        self.author = author
        self.domain = domain
        dict.__init__(self, review_id=review_id, product_name=product_name, text=text, author=author, date=date,
                      country=country,
                      polarity=polarity, domain=domain)

    @classmethod
    def from_json(cls, json):
        if 'review_id' in json:
            review_id = json['review_id']
        else:
            review_id = str(uuid.uuid4())
        try:
            date = datetime.strptime(json['date'], "%d %b %Y")
        except Exception:
            date = json['date']
        return cls(review_id, json['product_name'], json['text'], json['author'], date
                   , json['country'],
                   float(json['polarity']), json['domain'])

    def update_params(self, params: dict):
        self.__dict__.update(params)
        return self
