import uuid


class CommonStat(dict):
    def __init__(self, _id: str, positive: int, negative: int):
        self.id = uuid.uuid4().__str__()
        self.parent_id = _id
        self.positive = positive
        self.negative = negative
        super().__init__(parent_id=self.parent_id,
                         positive_reviews=self.positive, negative_reviews=self.negative)

    @classmethod
    def from_json(cls, json_data):
        return CommonStat(**json_data)
