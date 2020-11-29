from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.query import *
from sentiment_analysis.context_extractor.context_extractor import extract_contexts
from sentiment_analysis.readers.readers import read_lexicon
from sentiment_analysis.utils.utils import printProgressBar
import pandas as pd
import os
import itertools
import math
import time


def create_index(version):
    schema = Schema(polarity=NUMERIC(stored=True), content=TEXT,
                    postive_context=TEXT, negative_context=TEXT)
    if not os.path.exists("index/"+version):
        os.mkdir("index/"+version)

    ix = create_in("index/"+version, schema)

    writer = ix.writer(procs=6, limitmb=5000)

    # tweets = pd.read_csv(
    #     'resources/datasets/training.1600000.processed.noemoticon.csv', encoding='latin-1')
    # tweets.columns = ['polarity', 'id', 'date', 'flag', 'user', 'text']
    # reddit_data = pd.read_csv(
    #     'resources/datasets/Reddit_Data.csv', encoding="utf-8")
    # tweets_data = pd.read_csv(
    #     'resources/datasets/Twitter_Data.csv', encoding="utf-8")
    # tweets_data.columns = ['clean_comment', 'category']
    # tweets = (pd.concat([reddit_data[reddit_data.category !=
    #                                  0], tweets_data[tweets_data.category != 0]]))
    # tweets['category'] = tweets['category'].replace([0], 2)
    # tweets['category'] = tweets['category'].replace([1], 4)
    # tweets['category'] = tweets['category'].replace([-1], 0)
    # tweets.columns = ['text', 'polarity']
    tweets = pd.read_json('resources/datasets/reviews_Cell_Phones_and_Accessories_5.json',lines=True)
    tweets.columns = ['asin', 'helpful', 'polarity', 'text', 'reviewTime', 'reviewerID',
       'reviewerName', 'summary', 'unixReviewTime']
    tweets.polarity[tweets.polarity <= 2.5] = 0
    tweets.polarity[tweets.polarity > 2.5] = 4

    tweets = tweets[tweets.polarity != 2]
    tweets_len = len(tweets)
    i = 0
    print('Indexing Files')
    printProgressBar(i, tweets_len, prefix='Progress:',
                     suffix='Complete', length=100)
    for index, row in tweets.iterrows():
        if not math.isnan(row.polarity) and row.text == row.text:

            positive_context, negative_context = extract_contexts(
                str(row.text))
            positive_text = " ".join(
                list(itertools.chain.from_iterable(positive_context)))
            negative_text = " ".join(
                list(itertools.chain.from_iterable(negative_context)))
            writer.add_document(polarity=float(row.polarity),
                                content=row.text, postive_context=positive_text, negative_context=negative_text)

        i += 1
        printProgressBar(i, tweets_len, prefix='Progress:',
                         suffix='Complete', length=100)
    print('Commiting changes...')
    writer.commit()
    print('Completed')


if __name__ == "__main__":
    version = 'v5'
    start = time.time()
    create_index(version)
    end = time.time()
    print((end - start)/60000)
    

