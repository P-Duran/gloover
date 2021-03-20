import re
from typing import List

import pandas as pd
import spacy
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder

from gloover_model.readers.review_reader import ReviewReader
from gloover_model.serialization.product_feature import ProductFeature
from gloover_model.serialization.review import Review
from gloover_model.services.generic.language_proccesing import filter_tag


def __candidate_features__(text_reviews: List[str]):
    text_reviews = [filter_tag(t) for t in text_reviews]
    te = TransactionEncoder()
    te_ary = te.fit(text_reviews).transform(
        text_reviews)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    feature_candidates = apriori(
        df, max_len=2, min_support=0.05, use_colnames=True).itemsets.values
    feature_candidates = [list(feature) for feature in feature_candidates]
    single_feature = [f[0] for f in feature_candidates if len(f) == 1]
    complex_feature = [f for f in feature_candidates if len(f) != 1]
    return single_feature, complex_feature


def __feature_extractor__(reviews: List[str], simple_features, complex_features=None):
    if complex_features is None:
        complex_features = []

    def is_complex_feature(complex_features, text, result_complex):
        for f in complex_features:
            name = f[0] + ' ' + f[1]
            inv_name = f[1] + ' ' + f[0]
            n_count = len(re.findall(name, text))
            in_count = len(re.findall(inv_name, text))
            if (n_count < in_count):
                name = inv_name
            if not name in result_complex:
                result_complex[name] = 0
            result_complex[name] += n_count + in_count

    def is_simple_feature(doc, simple_features, text, nouns, result):
        for token in doc.to_json()['tokens']:
            token['word'] = text[token['start']:token['end']]
            if simple_features.__contains__(token['word']):
                token['adjectives'] = []
                nouns[token['id']] = token

        for token in doc.to_json()['tokens']:

            if token['head'] in nouns and 'JJ' in token['tag']:
                token['word'] = text[token['start']:token['end']]
                nouns[token['head']]['adjectives'] = nouns[token['head']
                                                     ]['adjectives'] + [token]
        for index in nouns:
            word_data = nouns[index]
            word = nouns[index]['word']
            data = {}
            if word in result:
                data = result[word]
                data['appearances'] += 1
                if len(word_data['adjectives']) != 0:
                    data['adj_count'] += 1
                data['adjectives'] += word_data['adjectives']
            else:
                data['appearances'] = 1
                if len(word_data['adjectives']) != 0:
                    data['adj_count'] = 1
                else:
                    data['adj_count'] = 0
                data['adjectives'] = word_data['adjectives']
            result[word] = data

    # ---------------------------------------------------------
    # Actual code
    nlp = spacy.load('en')
    result = {}
    result_complex = {}
    for text in reviews:
        text = text.lower()
        doc = nlp(text)
        nouns = {}
        is_complex_feature(complex_features, text, result_complex)
        is_simple_feature(doc, simple_features, text, nouns, result)

    return result, result_complex


def feature_selector(product_asin: str, reviews: List[Review], do_print=False):
    text_reviews = [review.text for review in reviews]
    simple, complex_features = __candidate_features__(text_reviews)
    result, result_complex = __feature_extractor__(text_reviews, simple, complex_features)
    if do_print:
        for e in result:
            print('\n------------' + e + '-------------')
            if not result[e]['adj_count'] / result[e]['appearances'] > 0.2:
                print('NOPE')
            print(result[e]['adj_count'] / result[e]['appearances'])
            print(result[e]['adj_count'], result[e]['appearances'])
            print([e['word'] for e in result[e]['adjectives']])
        for r in result_complex:
            print(r)
            if not result_complex[r] / len(reviews) > 0.1:
                print('NOPE')
            print(result_complex[r] / len(reviews))

    simple_features = [ProductFeature(product_asin, s, result[s]['adj_count'] / result[s]['appearances']) for s in
                       result if
                       result[s]['adj_count'] / result[s]['appearances'] >= 0.25]
    complex_features = [ProductFeature(product_asin, c, min(result_complex[c] / len(reviews), 1)) for c in
                        result_complex
                        if result_complex[c] / len(reviews) >= 0.1]

    return simple_features, complex_features


if __name__ == "__main__":
    # create_index()
    ""
