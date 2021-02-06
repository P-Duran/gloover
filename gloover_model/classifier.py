import os
import sys

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.svm import LinearSVC

from gloover_model.services.classifier.features import NegateWordsContext, PercentageContextNegative, PosTagCounter, \
    TotalSentimentScore

DEFAULT_MODEL_PATH = 'resources/models/classifierModel.mdl'
DEFAULT_DATASET_PATH = 'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json'


class Classifier:

    def __init__(self, model_path=DEFAULT_MODEL_PATH,
                 train_size=0.6, test_size=0.4, update_existent=False):
        self._update_existent = update_existent
        self.data_size = {"train": train_size, "test": test_size}
        self.model_path = model_path
        self.data = None
        self.data_train, self.data_test, self.y_train, self.y_true = None, None, None, None
        self.initialized = False
        self.model = None

    def intitialize(self, dataset=None):
        self.initialized = True
        if dataset:
            self.data = self._filter_dataset_(dataset)
            self.data_train, self.data_test, self.y_train, self.y_true = train_test_split(
                self.data['text'], self.data['polarity'], test_size=self.data_size["test"],
                train_size=self.data_size["train"])
        self._load_model()

    def test_model(self):
        if not self.initialized:
            raise Exception("Classifier not initialized")
        y_test = self.model.predict(self.data_test)
        return sklearn.metrics.accuracy_score(self.y_true, y_test)

    def classify(self, reviews):
        if not self.initialized:
            raise Exception("Classifier not initialized")
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
        if not self.data:
            raise Exception("No dataset was passed in init function")
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

    def _filter_dataset_(self, data):
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
    classifier = Classifier(test_size=0.2, train_size=0.2, update_existent=True)
    print(classifier.classify(['This is the best']))
