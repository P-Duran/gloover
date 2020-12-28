

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from sentiment_analysis.language_proccessing.language_proccesing import filter_tag
import spacy
from spacy import displacy


def algo():
    reviews = pd.read_json(
        'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json', lines=True)
    product_asin = reviews.asin.value_counts(
    )[reviews.asin.value_counts() > 200]
    print(product_asin)
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
    feature_candidates = [f[0] for f in feature_candidates if len(f) == 1]
    nlp = spacy.load('en')
    i = 0
    for text in big_number_reviews.reviewText:
        doc = nlp(text)
        nouns = {}
        spacy.displacy.serve(doc, style='dep')
        for token in doc.to_json()['tokens']:
            token['word'] = text[token['start']:token['end']]
            if feature_candidates.__contains__(token['word']):
                token['adjetives'] = []
                nouns[token['id']] = token

        for token in doc.to_json()['tokens']:

            if token['head'] in nouns and 'JJ' in token['tag']:
                token['word'] = text[token['start']:token['end']]
                nouns[token['head']]['adjetives'] = nouns[token['head']
                                                          ]['adjetives']+[token]
                
        print(nouns)
        if i > 3:
            break
        i += 1


if __name__ == "__main__":
    # create_index()
    algo()
