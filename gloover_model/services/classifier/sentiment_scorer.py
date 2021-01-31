from gloover_model.readers.lexicon_reader import read_lexicon
import numpy as np
import time
import json


class SentimentScorer():
    def __init__(self, lexicon_path):
        self.lexicon = read_lexicon(lexicon_path)
        try:
            with open('resources/lexicons/data.json') as f:
                self.dict = json.load(f)
        except Exception:
            with open('resources/lexicons/data.json', 'w') as f:
                self.dict = self.__to_dict(self.lexicon)
                json.dump(self.dict, f)

    def __to_dict(self, lexicon):
        dictionary = {}
        for i, row in lexicon.iterrows():
            word = row['word']
            if not dictionary.__contains__(word):
                dictionary[word] = row['polarity']
        return dictionary

    def word_sentiment_score(self, word, polarity):
        try:
            res = self.dict[word][polarity]
        except Exception:
            res = 0
        return res

    def sentence_sentiment_score(self, text, polarity='all'):
        score = 0
        score = np.sum(list(map(self.word_sentiment_score, text.split(), polarity)))
        return score


if __name__ == "__main__":
    sc = SentimentScorer('resources/lexicons/SentiWords_1.1.txt')
    start_time = time.time()
    print(sc.sentence_sentiment_score(
        "ut I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure? On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee "))
    print("--- %s seconds ---" % (time.time() - start_time))
