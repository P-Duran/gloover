from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
from mlxtend.frequent_patterns import apriori
import spacy
import re
from sentiment_analysis.language_proccessing.language_proccesing import filter_tag
from feature_extractor.data_reader.data_reader import Review_Reader


def candidate_features(reviews):
    text_reviews = reviews.reviewText
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


def feature_selector(reviews, simple_features, complex_features=[]):

    def is_complex_feature(complex_features, text, result_complex):
        for f in complex_features:
            name = f[0]+' '+f[1]
            inv_name = f[1]+' '+f[0]
            if not name in result_complex:
                result_complex[name] = 0
            result_complex[name] += len(re.findall(name, text))
            result_complex[name] += len(re.findall(inv_name, text))

    def is_simple_feature(doc, simple_features, text, nouns, result):
        for token in doc.to_json()['tokens']:
            token['word'] = text[token['start']:token['end']]
            if simple_features.__contains__(token['word']):
                token['adjetives'] = []
                nouns[token['id']] = token

        for token in doc.to_json()['tokens']:

            if token['head'] in nouns and 'JJ' in token['tag']:
                token['word'] = text[token['start']:token['end']]
                nouns[token['head']]['adjetives'] = nouns[token['head']
                                                          ]['adjetives']+[token]
        for index in nouns:
            word_data = nouns[index]
            word = nouns[index]['word']
            data = {}
            if word in result:
                data = result[word]
                data['appaerances'] += 1
                if len(word_data['adjetives']) != 0:
                    data['adj_count'] += 1
                data['adjetives'] += word_data['adjetives']
            else:
                data['appaerances'] = 1
                if len(word_data['adjetives']) != 0:
                    data['adj_count'] = 1
                else:
                    data['adj_count'] = 0
                data['adjetives'] = word_data['adjetives']
            result[word] = data

    # ---------------------------------------------------------
    # Actual code
    nlp = spacy.load('en')
    result = {}
    result_complex = {}
    for text in reviews.reviewText:
        text = text.lower()
        doc = nlp(text)
        nouns = {}
        is_complex_feature(complex_features, text, result_complex)
        is_simple_feature(doc, simple_features, text, nouns, result)

    return result, result_complex


def feature_extractor(reviews,do_print=False):
    simple, complex = candidate_features(reviews)
    result, result_complex = feature_selector(reviews, simple, complex)
    if do_print:
        for e in (result):
            print('\n------------'+e+'-------------')
            if not result[e]['adj_count']/result[e]['appaerances'] > 0.2:
                print('NOPE')
            print(result[e]['adj_count']/result[e]['appaerances'])
            print(result[e]['adj_count'], result[e]['appaerances'])
            print([e['word'] for e in result[e]['adjetives']])
        for r in (result_complex):
            print(r)
            if not result_complex[r] / len(reviews.reviewText) > 0.1:
                print('NOPE')
            print(result_complex[r] / len(reviews.reviewText))
    return [{'word': s, 'confidence': result[s]['adj_count']/result[s]['appaerances']} for s in result if result[s]['adj_count']/result[s]['appaerances'] > 0.2],  [{'word': c, 'confidence': result_complex[c] / len(reviews.reviewText)} for c in result_complex if result_complex[c] / len(reviews.reviewText) > 0.1]


if __name__ == "__main__":
    # create_index()
    rr = Review_Reader('resources/datasets/reviews_Cell_Phones_and_Accessories_5.json')
    reviews = rr.reviews_from_asin()
    feature_extractor(reviews)
