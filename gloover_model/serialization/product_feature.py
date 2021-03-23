import uuid


class FeatureType:
    SIMPLE = 'simple'
    COMPLEX = 'complex'


class ProductFeature(dict):
    def __init__(self, asin: str, word: str, confidence: float, type=str, id=None):
        if id is None:
            self.id = uuid.uuid4().__str__()
        else:
            self.id = id
        self.asin = asin
        self.confidence = confidence
        self.word = word
        self.type = type
        dict.__init__(self, id=self.id, asin=asin, confidence=confidence, word=word, type=type)

    @classmethod
    def from_json(cls, json_data):
        del json_data['_id']
        return ProductFeature(**json_data)
