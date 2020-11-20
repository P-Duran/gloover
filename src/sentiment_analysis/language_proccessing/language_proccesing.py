
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
import re
import string
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


def remove_noise(text, remove_punctuation=True, remove_stop_word=True):
    return word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words('english')
    cleaned_tokens = []
    try:
        tokenized_text = word_tokenize(text)
    except:
        print(f'error tokenizing -{text}-')
        return cleaned_tokens

    for token, tag in pos_tag(tokenized_text):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)
        token = re.sub(r'(.)\1{2,}', r'\1', token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        token = lemmatizer.lemmatize(token, pos)
        if len(token) > 0 and (token not in string.punctuation or not remove_punctuation) and (token.lower() not in stop_words or not remove_stop_word):
            cleaned_tokens.append(token.lower())
    return cleaned_tokens
