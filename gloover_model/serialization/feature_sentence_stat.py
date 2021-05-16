import uuid


class FeatureSentenceStat(dict):
    def __init__(self, _id: str, positive: int, negative: int, score: float):
        self.id = uuid.uuid4().__str__()
        self.feature_id = _id
        self.positive = positive
        self.negative = negative
        self.score = score
        super().__init__(id=self.id, feature_id=self.feature_id,
                         positive=self.positive, negative=self.negative, score=self.score)

    @classmethod
    def from_json(cls, json_data):
        return FeatureSentenceStat(**json_data)
