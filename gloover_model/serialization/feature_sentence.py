import uuid


class FeatureSentence(dict):
    def __init__(self, review_id: str, feature_id: str, asin: str, word: str, sentence: str, start: int, end: int,
                 id=None,
                 polarity=0):
        if id is None:
            self.id = uuid.uuid4().__str__()
        else:
            self.id = id
        self.review_id = review_id
        self.end = end
        self.start = start
        self.feature_id = feature_id
        self.word = word
        self.sentence = sentence
        self.polarity = polarity
        self.asin = asin
        dict.__init__(self, id=self.id, review_id=review_id, feature_id=feature_id, asin=asin, start=start,
                      end=end, word=word, sentence=sentence, polarity=polarity)

    @classmethod
    def from_json(cls, json_data):
        if '_id' in json_data:
            del json_data['_id']
        return FeatureSentence(**json_data)
