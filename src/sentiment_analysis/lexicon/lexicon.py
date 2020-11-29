from whoosh.index import open_dir
from sentiment_analysis.readers.readers import read_lexicon
import math as m
from whoosh.query.compound import And
from whoosh.query.terms import Term
from functools import partial
import swifter
import json
from whoosh import scoring


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
    sentiment_score = 0
    try:
        myquery = And([Term(fieldname, word), Term('polarity', 4)])
        docs = sorted(searcher.search(myquery).docs())
        positive_word_freq, terms_in_positive = get_termfreq_and_all_terms(
            docs, word, fieldname, searcher)
        pidf = m.log( searcher.doc_count() / len(docs))
        myquery = And([Term(fieldname, word), Term('polarity', 0)])
        docs = sorted(searcher.search(myquery).docs())
        negative_word_freq, terms_in_negative = get_termfreq_and_all_terms(
            docs, word, fieldname, searcher)
       
        nidf = m.log( searcher.doc_count() / len(docs))
        # print(positive_word_freq,terms_in_positive,negative_word_freq,terms_in_negative)
        sentiment_score = (m.log2((positive_word_freq*terms_in_negative*nidf ) /
                                  (negative_word_freq*terms_in_positive*pidf)))
    except:
        pass
    return sentiment_score


def positive_negative_sentiment_score(searcher, d, word):
    if (searcher.frequency('content', word) > 500 and (not word in d)):
        d[word] = {'all': sentiment_score(word, 'content', searcher), 'positive': sentiment_score(
            word, 'postive_context', searcher), 'negative': sentiment_score(word, 'negative_context', searcher)}


if __name__ == "__main__":
    version = 'v5'
    # start = time.time()
    # create_index(version)
    # end = time.time()
    # print((end - start)/60000)

    ix = open_dir("index/"+version)
    searcher = ix.searcher()
    # print(ix.schema)
    lexicon = read_lexicon('resources/lexicons/SentiWords_1.1.txt')
    test_words = ['useful', 'great', 'beautiful', 'nice', 'good',
                  'honest', 'terrible', 'shame', 'bad', 'ugly', 'negative']
    # print(lexicon.word)
    # d = {}
    # func = partial(positive_negative_sentiment_score, searcher,d )
    # tosave = lexicon.word.swifter.apply(func)
    # with open('data2.json', 'w') as fp:
    #     json.dump(d, fp)
    for word in test_words:
        if (searcher.frequency('content', word)):
            try:
                print('----'+word+'----')

                print(searcher.frequency('content', word))
                print('All contexts:      ' +
                      str(sentiment_score(word, 'content', searcher)))
                print('Positive contexts: ' +
                      str(sentiment_score(word, 'postive_context', searcher)))
                print('Negative contexts: ' +
                      str(sentiment_score(word, 'negative_context', searcher)))
            except:
                pass
    searcher.close()
