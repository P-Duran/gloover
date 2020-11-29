from sklearn.base import BaseEstimator, TransformerMixin
from sentiment_analysis.context_extractor.context_extractor import extract_contexts
from sentiment_analysis.sentiment_classifier.sentiment_classifier import SentimentClassifier
import swifter
import itertools

class TotalSentimentScore(BaseEstimator, TransformerMixin):
    """Takes in dataframe, extracts road name column, outputs average word length"""

    def __init__(self):
        self.senti_class = SentimentClassifier()

        pass

    def average_word_length(self, text):
        """Helper code to compute average word length of a name"""
        p,n = extract_contexts(text)
        pscore = 0
        pnscore = 0
        if len(p)>0:
            pscore = self.senti_class.sentence_sentiment_score(' '.join(list(itertools.chain.from_iterable(p))),polarity='positive')
        if len(n)> 0:
            pnscore = self.senti_class.sentence_sentiment_score(' '.join(list(itertools.chain.from_iterable(n))),polarity='negative')
        return pscore+pnscore

    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""
        return df.swifter.apply(self.average_word_length).values.reshape(df.size, 1)

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self

class PercentageContextNegative(BaseEstimator, TransformerMixin):
    """Takes in dataframe, extracts road name column, outputs average word length"""

    def __init__(self):

        pass

    def average_word_length(self, text):
        """Helper code to compute average word length of a name"""
        p,n = extract_contexts(text)
        
        return len(n)/(len(n)+len(p))

    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""
        return df.swifter.apply(self.average_word_length).values.reshape(df.size, 1)

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self