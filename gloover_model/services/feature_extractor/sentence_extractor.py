from gloover_model.services.feature_extractor.feature_selector import feature_selector
from gloover_model.readers.review_reader import ReviewReader
from nltk import sent_tokenize
import spacy
import re
import os.path
import json


def __search_simple_in_text__(text, review_id, words, nlp, result={}):
    sentences = sent_tokenize(text.lower())
    for sentence in sentences:
        doc = nlp(sentence)
        for token in doc.to_json()['tokens']:
            token_word = sentence[token['start']:token['end']]
            if words.__contains__(token_word):
                if not review_id in result:
                    result[review_id] = {}
                if not token_word in result[review_id]:
                    result[review_id][token_word] = []
                result[review_id][token_word] += [
                    {'sentence': sentence, 'feature-start': token['start'], 'feature-end': token['end']}]


def __search_complex_in_text__(text, review_id, words, nlp, result={}):
    sentences = sent_tokenize(text.lower())
    for sentence in sentences:
        for feature in words:
            p = re.compile(feature)
            for m in p.finditer(sentence):
                start, end = m.span()
                if not review_id in result:
                    result[review_id] = {}
                if not feature in result[review_id]:
                    result[review_id][feature] = []
                result[review_id][feature] += [
                    {'sentence': sentence, 'feature-start': start, 'feature-end': end}]


def sentence_extractor(path=None):
    nlp = spacy.load('en')
    features_file = 'generated/features/features.json'
    rr = ReviewReader(path)
    reviews = rr.reviews_from_asin()
    if not os.path.isfile(features_file) and path:
        features = feature_selector(reviews, do_save=True)
    else:
        with open(features_file) as f:
            features = json.load(f)

    simple_features = [sf['word'] for sf in features['simple']]
    complex_features = [sf['word'] for sf in features['complex']]
    data = {}
    for index, row in reviews.iterrows():
        __search_simple_in_text__(row.reviewText, row.unixReviewTime, simple_features, nlp, data)
        __search_complex_in_text__(row.reviewText, row.unixReviewTime, complex_features, nlp, data)
    return data


if __name__ == "__main__":
    # create_index())
    print(sentence_extractor(
        'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json'))