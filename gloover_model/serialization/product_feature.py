import uuid


class ProductFeature(dict):
    def __init__(self, asin: str, word: str, confidence: float):
        self.feature_id = uuid.uuid4().__str__()
        self.asin = asin
        self.confidence = confidence
        self.word = word
        dict.__init__(self, feature_id=self.feature_id, asin=asin, confidence=confidence, word=word)
