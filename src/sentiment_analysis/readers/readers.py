import pandas as pd

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
