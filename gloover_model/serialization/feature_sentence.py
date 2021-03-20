class FeatureSentence(dict):
    def __init__(self, review_id: str, feature_id: str, word: str, sentence: str, start: int, end: int):
        self.review_id = review_id
        self.end = end
        self.start = start
        self.feature_id = feature_id
        self.word = word
        self.sentence = sentence
        dict.__init__(self, review_id=review_id, feature_id=feature_id, start=start, end=end, sentence=sentence)
