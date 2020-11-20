from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.query import *
from sentiment_analysis.context_extractor.context_extractor import extract_contexts
from sentiment_analysis.readers.readers import read_lexicon
import pandas as pd
import os
import itertools
import math
import time

def create_index():
    schema = Schema(id=NUMERIC(stored=True, bits=64),
                    polarity=NUMERIC(stored=True), content=TEXT, postive_context=TEXT, negative_context=TEXT)
    if not os.path.exists("index"):
        os.mkdir("index")

    ix = create_in("index", schema)

    writer = ix.writer()

    tweets = pd.read_csv(
        'resources/datasets/training.1600000.processed.noemoticon.csv', encoding='latin-1')

    tweets.columns = ['polarity', 'id', 'date', 'flag', 'user', 'text']
    tweets = tweets[tweets.polarity != 2]
    tweets_len = len(tweets)
    for index, row in tweets.iterrows():
        positive_context, negative_context = extract_contexts(row.text)
        positive_text = " ".join(
            list(itertools.chain.from_iterable(positive_context)))
        negative_text = " ".join(
            list(itertools.chain.from_iterable(negative_context)))
        try:
            writer.add_document(id=row.id, polarity=row.polarity,
                                content=row.text, postive_context=positive_text, negative_context=negative_text)
        except:
            print(row)
        print("Progress {:2.1%}".format(index/tweets_len), end="\r")

    writer.commit()


def get_termfreq_and_all_terms(docs, word, fieldname, searcher):

    postings = searcher.postings(fieldname, word)
    positive_word_freq = 0
    terms_in_positive = 0
    for docId in docs:
        terms_in_positive += searcher.doc_field_length(docId, fieldname)
        postings.skip_to(docId)
        if postings.id() == docId:
            positive_word_freq += postings.weight()
        
    return positive_word_freq, terms_in_positive


def sentiment_score(word, fieldname, searcher):

    myquery = And([Term(fieldname, word), Term('polarity', 4)])
    docs = sorted(searcher.search(myquery).docs())
    positive_word_freq, terms_in_positive = get_termfreq_and_all_terms(
        docs, word, fieldname, searcher)

    myquery = And([Term(fieldname, word), Term('polarity', 0)])
    docs = sorted(searcher.search(myquery).docs())
    negative_word_freq, terms_in_negative = get_termfreq_and_all_terms(
        docs, word, fieldname, searcher)
    print(positive_word_freq,terms_in_positive, negative_word_freq,terms_in_negative)
    sentiment_score = (math.log2((positive_word_freq*terms_in_negative) /
                                 (negative_word_freq*terms_in_positive)))

    return sentiment_score


if __name__ == "__main__":
    start = time.time()
    create_index()
    end = time.time()
    print((end - start)/60000)
    
    # ix = open_dir("index")
    # searcher = ix.searcher()
    # print(ix.schema)
    # for word in ['great','beautiful','nice','good','honest','terrible','shame','bad','ugly','negative']:
    #     print(word)
    #     try:
    #         print(sentiment_score(word, 'content', searcher))
    #         print(sentiment_score(word, 'postive_context', searcher))
    #         print(sentiment_score(word, 'negative_context', searcher))
    #     except:
    #         pass
    # searcher.close()
