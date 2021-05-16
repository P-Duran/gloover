import uuid

from gloover_service.utils.logger import Logger


class FeatureType:
    SIMPLE = 'simple'
    COMPLEX = 'complex'


class ProductFeature(dict):
    def __init__(self, asin: str, word: str, confidence: float, appearances: int, type=str, id=None):
        if id is None:
            self.id = uuid.uuid4().__str__()
        else:
            self.id = id
        self.asin = asin
        self.confidence = confidence
        self.word = word
        self.type = type
        self.appearances = appearances
        Logger.log_warning(self.id)
        dict.__init__(self, id=self.id, asin=asin, word=word, type=type, appearances=appearances, confidence=confidence)

    @classmethod
    def from_json(cls, json_data):
        del json_data['_id']
        Logger.log_warning(json_data)
        return ProductFeature(**json_data)
