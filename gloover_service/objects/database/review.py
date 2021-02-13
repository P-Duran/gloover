from datetime import datetime


class Review(object):
    def __init__(self, product_name: str, text: str, user_name: str, date: datetime, country: str, polarity: float,
                 webpage: str):
        self.polarity = polarity
        self.country = country
        self.date = date
        self.text = text
        self.product_name = product_name
        self.user_name = user_name
        self.webpage = webpage

    @classmethod
    def from_json(cls, json):
        return cls(json['productName'], json['text'], json['userName'],
                   datetime.strptime(json['date'], "%d %m %Y"), json['country'],
                   float(json['polarity']), json['webpage'])
