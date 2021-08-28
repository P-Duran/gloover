import re
from typing import List

import spacy
from nltk import sent_tokenize

from gloover_model.serialization.feature_sentence import FeatureSentence
from gloover_model.serialization.product_feature import ProductFeature
from gloover_model.serialization.review import Review
from gloover_service.utils.logger import Logger


def __search_simple_in_text__(review: Review, words, nlp, result=None):
    text = review.text
    review_id = review.review_id
    date = review.date
    if result is None:
        result = {}
    sentences = sent_tokenize(text.lower())
    for sentence in sentences:
        doc = nlp(sentence)
        for token in doc.to_json()['tokens']:
            token_word = sentence[token['start']:token['end']]
            if words.__contains__(token_word):
                if review_id not in result:
                    result[review_id] = {}
                if token_word not in result[review_id]:
                    result[review_id][token_word] = []
                result[review_id][token_word] += [
                    {'sentence': sentence, 'feature-start': token['start'], 'feature-end': token['end'], "date": date}]


def __search_complex_in_text__(review: Review, words, nlp, result=None):
    text = review.text
    review_id = review.review_id
    date = review.date
    if result is None:
        result = {}
    sentences = sent_tokenize(text.lower())
    for sentence in sentences:
        for feature in words:
            p = re.compile(feature)
            for m in p.finditer(sentence):
                start, end = m.span()
                if review_id not in result:
                    result[review_id] = {}
                if feature not in result[review_id]:
                    result[review_id][feature] = []
                result[review_id][feature] += [
                    {'sentence': sentence, 'feature-start': start, 'feature-end': end, "date": date}]


def sentence_extractor(reviews: List[Review], asin: str, s_features: List[ProductFeature],
                       c_features: List[ProductFeature]):
    nlp = spacy.load('en')
    simple_features = [f.word for f in s_features]
    complex_features = [f.word for f in c_features]
    search_array = s_features + c_features
    data = {}
    for review in reviews:
        __search_simple_in_text__(review, simple_features, nlp, data)
        __search_complex_in_text__(review, complex_features, nlp, data)
    result = []
    for review_id in data.keys():
        for feature in data[review_id].keys():
            for feature_sentence in data[review_id][feature]:
                try:
                    feature_id = [f.id for f in search_array if f.word == feature][0]
                    result.append(FeatureSentence(review_id, feature_id, asin, feature, feature_sentence['sentence'],
                                                  feature_sentence['feature-start'],
                                                  feature_sentence['feature-end'], feature_sentence['date']))
                except Exception:
                    Logger.log_error("'" + feature + "'was not found as a ProductFeature")
    return result


if __name__ == "__main__":
    # create_index())
    ""
