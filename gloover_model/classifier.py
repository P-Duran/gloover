import sys

import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split
import sklearn
import numpy as np
from sklearn.pipeline import FeatureUnion, Pipeline
from gloover_model.services.classifier.features import NegateWordsContext, PercentageContextNegative, PosTagCounter, \
    TotalSentimentScore
import joblib
import os

DEFAULT_MODEL_PATH = 'resources/models/classifierModel.mdl'
DEFAULT_DATASET_PATH = 'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json'


class Classifier:

    def __init__(self, dataset_path=DEFAULT_DATASET_PATH, model_path=DEFAULT_MODEL_PATH,
                 train_size=0.6, test_size=0.4, update_existent=False):
        self._update_existent = update_existent
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.data = self._load_training_data()
        self.data_train, self.data_test, self.y_train, self.y_true = train_test_split(
            self.data['text'], self.data['polarity'], test_size=test_size, train_size=train_size)
        self.model = self._load_model()

    def test_model(self):
        y_test = self.model.predict(self.data_test)
        return sklearn.metrics.accuracy_score(self.y_true, y_test)

    def classify(self, reviews):
        return self.model.predict(pd.Series(reviews))

    def _save_model(self, model):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(model, self.model_path)

    def _load_model(self):
        if not self._update_existent:
            try:
                return joblib.load(self.model_path)
            except Exception:
                print('Problem loading the model, a new one would be trained', file=sys.stderr)
        print('Problem loading the model, a new one would be trained', file=sys.stderr)
        ppl_neg = Pipeline([('_NEG words', NegateWordsContext()),
                            ('word_ngrams', CountVectorizer(ngram_range=(1, 4), analyzer='word')), ])
        ppl = Pipeline([
            ('text_features', FeatureUnion([
                ('postag', PosTagCounter()),
                # ('v', Pipeline(
                #     [('efe', WordsExtractor()), ('ge', CountVectorizer(ngram_range=(1, 4), analyzer='char'))])),
                ('char_ngrams', CountVectorizer(
                    ngram_range=(1, 4), analyzer='char')),
                ('neg', ppl_neg),
                ('tfidf', TfidfVectorizer()),
                ('%', PercentageContextNegative()),
                ('ss', TotalSentimentScore()),

            ])),
            ('clf', LinearSVC())
        ])
        model = ppl.fit(self.data_train, self.y_train)
        self._save_model(model)
        return model

    def _load_training_data(self):
        data = pd.read_json(self.dataset_path, lines=True)
        data.columns = ['reviewerID', 'asin', 'reviewerName', 'helpful',
                        'text', 'polarity', 'summary', 'unixReviewTime', 'reviewTime']
        data.polarity[data.polarity < 2.5] = -1
        data.polarity[data.polarity >= 2.5] = 1
        data = data[(data.polarity == 1) | (data.polarity == -1)]
        labels = data.groupby('polarity').text.unique()
        # Sort the over-represented class to the head.
        labels = labels[labels.apply(len).sort_values(ascending=False).index]
        excess = len(labels.iloc[0]) - len(labels.iloc[1])
        remove = np.random.choice(labels.iloc[0], excess, replace=False)
        df2 = data[~data.text.isin(remove)]
        return df2


if __name__ == "__main__":
    classifier = Classifier(test_size=0.05, train_size=0.05, update_existent=True)
    print(classifier.classify(['This is the best']))
