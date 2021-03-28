import os
import uuid
from typing import List

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.svm import LinearSVC

from gloover_model.serialization.review import Review
from gloover_model.services.classifier.features import NegateWordsContext, PercentageContextNegative, PosTagCounter, \
    TotalSentimentScore
from gloover_service.utils.logger import Logger

DEFAULT_MODEL_PATH = 'resources/models/'
DEFAULT_DATASET_PATH = 'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json'


class Classifier:

    def __init__(self):
        self.model = None
        self.model_id = None

    def classify(self, reviews):
        return self.model.predict(pd.Series(reviews))

    def load_model(self, model_id: str):
        try:
            model_path = DEFAULT_MODEL_PATH + '/' + model_id + '.mdl'
            self.model = joblib.load(model_path)
            Logger.log_warning("The model with id '" + model_id + "' was loaded into the classifier")
            self.model_id = model_id
            return model_id
        except Exception:
            raise Exception("The model with id '" + model_id + "' could not be loaded")

    def create_model(self, dataset: List[Review], model_id=None):
        data, data_train, data_test, y_train, y_true = self._initialize_required_data(dataset)
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
        model = ppl.fit(data_train, y_train)
        if model_id is None:
            model_id = uuid.uuid4().__str__()
        self._save_model(model, model_id)
        accuracy = self._test_model(data_test, y_true)
        return model_id, accuracy

    def _initialize_required_data(self, dataset: List[Review], train_size=0.6, test_size=0.4):
        data = self._filter_dataset_(pd.DataFrame(dataset))
        data_train, data_test, y_train, y_true = train_test_split(
            data['text'], data['polarity'], test_size=test_size,
            train_size=train_size)
        return data, data_train, data_test, y_train, y_true

    def _test_model(self, data_test, y_true):
        """Probably better to test the model once you have created it"""
        y_test = self.model.predict(data_test)
        return sklearn.metrics.accuracy_score(y_true, y_test)

    def _save_model(self, model, model_id: str):
        model_path = DEFAULT_MODEL_PATH + "/" + model_id + ".mdl"
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(model, model_path)

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
    ""
    # classifier = Classifier(test_size=0.2, train_size=0.2, update_existent=True)
    # print(classifier.classify(['This is the best']))
