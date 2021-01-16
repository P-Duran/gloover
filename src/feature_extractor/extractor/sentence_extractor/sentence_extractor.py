from feature_extractor.extractor.word_extractor.extractor import feature_extractor
from feature_extractor.data_reader.data_reader import Review_Reader
from nltk import sent_tokenize, word_tokenize
import spacy
import re


def search_simple_in_text(text, review_id, words, nlp, result={}):
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
                    {'sentence': sentence, 'feature-start': token['start'], 'feature-end':token['end']}]


def search_complex_in_text(text, review_id, words, nlp, result={}):
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


def sentence_extractor(path):
    nlp = spacy.load('en')
    rr = Review_Reader(path)
    reviews = rr.reviews_from_asin()
    features = feature_extractor(reviews)
    simple_features = [sf['word'] for sf in features['simple']]
    complex_features = [sf['word'] for sf in features['complex']]
    data = {}
    for index, row in reviews.iterrows():
        search_simple_in_text(row.reviewText, row.unixReviewTime,simple_features , nlp, data)
        search_complex_in_text(row.reviewText, row.unixReviewTime, complex_features, nlp, data)
    return data


if __name__ == "__main__":
    # create_index())
    print(sentence_extractor(
        'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json'))
