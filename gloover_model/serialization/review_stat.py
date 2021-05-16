import uuid


class ReviewStat(dict):
    def __init__(self, _id: str, positive_reviews: int, negative_reviews: int):
        self.id = uuid.uuid4().__str__()
        self.asin = _id
        self.positive_reviews = positive_reviews
        self.negative_reviews = negative_reviews
        super().__init__(id=self.id, asin=self.asin,
                         positive_reviews=self.positive_reviews, negative_reviews=self.negative_reviews)

    @classmethod
    def from_json(cls, json_data):
        return ReviewStat(**json_data)
