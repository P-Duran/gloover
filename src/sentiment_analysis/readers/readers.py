import pandas as pd
from punctuator import Punctuator
from multiprocessing import Pool
import sys


def read_lexicon(file_path):
    f = open(file_path, "r")
    words_sentiment = f.read().split("\n")
    words_sentiment = words_sentiment[397:]
    word_list = []
    pos_tag_list = []
    polarity_word_list = []
    for ws in words_sentiment:
        try:
            [word_pos, polarity] = ws.split('\t')
            polarity = float(polarity)
            word, pos = word_pos.split('#')
            word_list.append(word)
            pos_tag_list.append(pos)
            polarity_word_list.append(polarity)
        except:
            print(ws)

    leixon = {'word': word_list,
              'pos': pos_tag_list, 'polarity': polarity_word_list
              }
    df = pd.DataFrame(leixon, columns=['word', 'pos', 'polarity'])
    return df


if __name__ == "__main__":

    reddit_data = pd.read_csv(
        'resources/datasets/Reddit_Data.csv', encoding="utf-8")
    tweets_data = pd.read_csv(
        'resources/datasets/Twitter_Data.csv', encoding="utf-8")
    tweets_data.columns = ['clean_comment', 'category']
    tweets = (pd.concat([reddit_data[reddit_data.category !=
                                     0], tweets_data[tweets_data.category != 0]]))
    tweets['category'] = tweets['category'].replace([0], 2)
    tweets['category'] = tweets['category'].replace([1], 4)
    tweets['category'] = tweets['category'].replace([-1], 0)
    tweets.columns = ['text', 'polarity']
    p = Punctuator('resources/models/Demo-Europarl-EN.pcl')
    filed = open("demofile2.txt", "a")
    sys.stdout = filed
    iterator = tweets.iterrows()
    i_len = len(tweets)
    percentage = [0]

    def f(data):
        i, row = data
        try:
            tweets.at[i, 'text'] = p.punctuate(row.text)

        except Exception as e:
            print(str(e))
            filed.flush()
        percentage[0] += 1
    with Pool() as p:
        p.map(f, iterator)
# 6304
    filed.close()
    tweets.to_csv("resources/datasets/out.csv")
    print(pd.read_csv("resources/datasets/out.csv"))
