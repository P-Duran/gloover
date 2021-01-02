

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
from sentiment_analysis.classifier.features.features import NegateWordsContext, PercentageContextNegative, PosTagCounter, TotalSentimentScore, WordsExtractor
from sklearn.metrics import f1_score, precision_score, recall_score

if __name__ == "__main__":
    data = pd.read_json(
        'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json', lines=True)
    data.columns = ['asin', 'helpful', 'polarity', 'text', 'reviewTime', 'reviewerID',
                    'reviewerName', 'summary', 'unixReviewTime']
    data.polarity[data.polarity < 2.5] = -1
    data.polarity[data.polarity >= 2.5] = 1

    data = data[(data.polarity == 1) | (data.polarity == -1)]
    # data = pd.read_csv(
    #     'resources/datasets/Reddit_Data.csv', encoding="utf-8")
    # data.columns = ['text', 'polarity']
    # data = data[data.polarity != 0]
    labels = data.groupby('polarity').text.unique()
    # Sort the over-represented class to the head.
    labels = labels[labels.apply(len).sort_values(ascending=False).index]
    excess = len(labels.iloc[0]) - len(labels.iloc[1])
    remove = np.random.choice(labels.iloc[0], excess, replace=False)
    df2 = data[~data.text.isin(remove)]
    print(df2.polarity.value_counts())

    data_len = len(data)
    ppl_neg = Pipeline([('_NEG words', NegateWordsContext()),
                        ('word_ngrams', CountVectorizer(ngram_range=(1, 4), analyzer='word')), ])
    ppl = Pipeline([
        ('text_features', FeatureUnion([
            ('postag', PosTagCounter()),
            # ('v', Pipeline(
            #     [('efe', WordsExtractor()), ('ge', CountVectorizer(ngram_range=(1, 4), analyzer='char'))])),
            ('char_ngrams', CountVectorizer(ngram_range=(1, 4), analyzer='char')),
            ('neg', ppl_neg),
            ('tfidf', TfidfVectorizer()),
            ('%', PercentageContextNegative()),
            ('ss', TotalSentimentScore()),

        ])),
        ('clf',   LinearSVC())
    ])

    data_train, data_test, y_train, y_true=train_test_split(
        df2['text'], df2['polarity'], test_size=0.1, train_size=0.1)
    model=ppl.fit(data_train, y_train)
    y_test=model.predict(data_test)
    print(y_test)
    newvals=pd.Series([ "There were few scratches on the frame and the plastic is poor quality after removing the screws they are barely can be screwed in second time. The instructions are misleading - there are probably other bike models available and some of the assembly instruction don't apply to the model we bought.overall quality is less than average ",
                        ]
                        )
    result=model.predict(newvals)
    print(sklearn.metrics.accuracy_score([-1],
                                         result))
    print(sklearn.metrics.accuracy_score(y_true, y_test))
    print(f1_score(y_test, y_true, average="macro"))
    print(precision_score(y_test, y_true, average="macro"))
    print(recall_score(y_test, y_true, average="macro"))
    # plot_decision_regions(X=X.values,
    #                       y=y.values,
    #                       clf=m1,
    #                       legend=2)

    # Update plot object with X/Y axis labels and Figure Titl
    # plt.xlabel(X.columns[0], size=14)
    # plt.title('SVM Decision Region Boundary', size=16)
