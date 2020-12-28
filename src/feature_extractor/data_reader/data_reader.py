

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from sentiment_analysis.language_proccessing.language_proccesing import filter_tag, remove_noise
import spacy
from spacy import displacy
import re


def algo():
    reviews = pd.read_json(
        'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json', lines=True)
    product_asin = reviews.asin.value_counts(
    )[reviews.asin.value_counts() > 200]
    big_number_reviews = reviews[reviews.asin == product_asin.index[1]]
    text_reviews = big_number_reviews.reviewText
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
    nlp = spacy.load('en')
    i = 0
    result = {}
    result_complex = {}
    for text in big_number_reviews.reviewText:
        text = text.lower()
        doc = nlp(text)
        nouns = {}
        for f in complex_feature:
            name = f[0]+' '+f[1]
            inv_name = f[1]+' '+f[0]
            if not name in result_complex:
                result_complex[name] = 0
            result_complex[name] += len(re.findall(name, text))
            result_complex[name] += len(re.findall(inv_name, text))

        #spacy.displacy.serve(doc, style='dep')
        for token in doc.to_json()['tokens']:
            token['word'] = text[token['start']:token['end']]
            if single_feature.__contains__(token['word']):
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
        i += 1
    for e in (result):
        print('\n------------'+e+'-------------')
        if result[e]['adj_count']/result[e]['appaerances'] > 0.2:
            print(result[e]['adj_count']/result[e]['appaerances'])
            print(result[e]['adj_count'], result[e]['appaerances'])
            print([e['word'] for e in result[e]['adjetives']])
    for r in (result_complex):
        print(r)
        if result_complex[r] / len(big_number_reviews.reviewText) > 0.1:
            print(result_complex[r] / len(big_number_reviews.reviewText))


if __name__ == "__main__":
    # create_index()
    algo()
