

import pandas as pd
from sklearn.svm import LinearSVC
from matplotlib import pyplot as plt
from mlxtend.plotting import plot_decision_regions
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split
import sklearn
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.pipeline import FeatureUnion, Pipeline
from analyzer.sentiment_analysis.classifier.features.features import NegateWordsContext, PercentageContextNegative, PosTagCounter, TotalSentimentScore, WordsExtractor
from sklearn.metrics import f1_score, precision_score, recall_score
import joblib
import sys
import os
import errno

DEFAULT_MODEL_PATH = 'resources/models/classifierModel.mdl'
DEFAULT_DATASET_PATH = 'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json'

class Classifier:

    
    def __init__(self, dataset_path = DEFAULT_DATASET_PATH, model_path = DEFAULT_MODEL_PATH, train_size = 0.6, test_size = 0.4):
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.data = self.__load_training_data__(dataset_path)
        self.data_train, self.data_test, self.y_train, self.y_true = train_test_split(
            self.data['text'], self.data['polarity'], test_size=test_size, train_size=train_size)
        self.model = self.__load_model__(model_path)

    def test_model(self):
        y_test = self.model.predict(self.data_test)
        return sklearn.metrics.accuracy_score(self.y_true, y_test)

    def classify(self, reviews):
        return self.model.predict(pd.Series(reviews))

    def __save_model__(self,model): 
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(model, self.model_path)

    def __load_training_data__(self, path=None):
        data = pd.read_json(path, lines=True)
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

    def __load_model__(self,model_path = None):
        try:
            print('Loading model...')
            return joblib.load(model_path)
        except Exception as e:
            print('Problem loading the model, a new one would be trained')
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
                ('clf',   LinearSVC())
            ])
            model = ppl.fit(self.data_train, self.y_train)
            self.__save_model__(model)
            return model


if __name__ == "__main__":
    classifier = Classifier(
        'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json', test_size=0.05, train_size=0.05)
    print(classifier.classify(['This is the best']))
