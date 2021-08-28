from sklearn.base import BaseEstimator, TransformerMixin
from gloover_model.services.classifier.context_extractor import extract_contexts, extract_ordered_contexts
from gloover_model.services.classifier.sentiment_scorer import SentimentScorer
import itertools
from gloover_model.services.generic.language_proccesing import sentence_pos_tokenize, remove_noise
import numpy as np
import scipy as sp
import swifter #Do Not Delete


class TotalSentimentScore(BaseEstimator, TransformerMixin):
    """Calculates sentiment score based on sentiwords1_1"""

    def __init__(self):
        self.senti_class = SentimentScorer('resources/lexicons/SentiWords_1.1.txt')

        pass

    def sentiment_score(self, text):
        """Helper code to compute average word length of a name"""
        p, n = extract_contexts(text)
        pscore = 0
        pnscore = 0
        if len(p) > 0:
            pscore = self.senti_class.sentence_sentiment_score(
                ' '.join(list(itertools.chain.from_iterable(p))), polarity='positive')
        if len(n) > 0:
            pnscore = self.senti_class.sentence_sentiment_score(
                ' '.join(list(itertools.chain.from_iterable(n))), polarity='negative')
        return pscore + pnscore

    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""
        return df.swifter.apply(self.sentiment_score).values.reshape(df.size, 1)

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self


class PercentageContextNegative(BaseEstimator, TransformerMixin):
    """Eso mismo"""

    def __init__(self):
        # No initialization needed
        pass

    def percentage_negative_context(self, text):
        """Helper code to compute average word length of a name"""
        p, n = extract_contexts(text)

        return len(n) / (len(n) + len(p))

    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""
        return df.swifter.apply(self.percentage_negative_context).values.reshape(df.size, 1)

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self


class NegateWordsContext(BaseEstimator, TransformerMixin):
    """Transforms text into text with negative context words with a NEG in front"""

    def __init__(self):
        # No initialization needed
        pass

    def add_negated_tag_words(self, text):
        c = extract_ordered_contexts(text)
        result = ""
        for sen in c:
            polarity, list_words = sen
            if (polarity == 'NEG'):
                result += '_NEG '.join(list_words) + ' '
            else:
                result += ' '.join(list_words) + ' '
        return result

    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""
        a = df.swifter.apply(self.add_negated_tag_words)
        return a

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self


class PosTagCounter(BaseEstimator, TransformerMixin):
    """Number of nouns, verbs and adjectives"""

    def __init__(self):
        # No initialization needed
        pass

    def pos_tag_count(self, text):
        """Helper code to compute average word length of a name"""
        _, counts = sentence_pos_tokenize(text)

        return [counts['n'], counts['v'], counts['a']]

    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""
        values = np.array(df.swifter.apply(self.pos_tag_count).values)
        narray = [e for e in values]
        result = sp.sparse.csr_matrix(np.array(narray))
        return result

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self


class WordsExtractor(BaseEstimator, TransformerMixin):
    """Extrae el texto en tokens"""

    def __init__(self):
        # No initialization needed
        pass

    def word_extractor(self, text):
        """Helper code to compute average word length of a name"""
        tokens = remove_noise(text)

        return tokens

    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""

        return df.swifter.apply(self.word_extractor)

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self


class WordsExtractor(BaseEstimator, TransformerMixin):
    """Takes in dataframe, extracts road name column, outputs average word length"""

    def __init__(self):
        # No initialization needed
        pass

    def transform(self, df, y=None):
        """The workhorse of this feature extractor"""

        return df.swifter.apply(self.word_extractor)

    def fit(self, df, y=None):
        """Returns `self` unless something different happens in train and test"""
        return self
