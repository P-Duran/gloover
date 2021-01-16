from feature_extractor.extractor.word_extractor.extractor import feature_extractor
from feature_extractor.data_reader.data_reader import Review_Reader
from nltk import sent_tokenize, word_tokenize
import spacy


def search_in_text(text, review_id, words, nlp, result={}):
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


def sentence_extractor(path):
    nlp = spacy.load('en')
    rr = Review_Reader(path)
    reviews = rr.reviews_from_asin()
    simple_features, complex_features = feature_extractor(reviews)
    print(reviews)
    data = {}
    for index, row in reviews.iterrows():
        search_in_text(row.reviewText, row.unixReviewTime, [sf['word']
                                                            for sf in simple_features], nlp, data)
    return data


if __name__ == "__main__":
    # create_index())
    sentence_extractor('resources/datasets/reviews_Cell_Phones_and_Accessories_5.json')
