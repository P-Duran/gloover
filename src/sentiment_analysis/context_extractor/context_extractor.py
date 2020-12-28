from sentiment_analysis.language_proccessing.language_proccesing import remove_noise
from nltk.collections import OrderedDict


def __partition(alist, indices):
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]


def __get_next(neg_indices, all_indices):
    segmentation = []
    for i in neg_indices:
        i_index = all_indices.index(i)
        segmentation.append(i)
        if i_index+1 < len(all_indices):
            segmentation.append(all_indices[i_index+1])
    return list(OrderedDict.fromkeys(segmentation))


def extract_contexts(text, ordered=False):
    text = text.lower()
    # p = Punctuator('resources/models/Demo-Europarl-EN.pcl')
    # text = (p.punctuate(text))
    punctuation = ['.', ',', ';', ':', ';', '!', '?', 'but']
    negation_words = ["n't", "never", "no", "nothing", "nowhere", "noone", "nonenot",
                      "havent", "haven't", "hasnt", "hasn't" "hadnt", "hadn't",
                      "cant", "can't", "couldnt", "couldn't", "shouldnt", "shouldn't",
                      "wont", "won't", "wouldnt", "wouldn't", "dont", "don't", "doesnt",
                      "doesn't", "didnt", "didn't", "isnt", "isn't", "arent", "aren't", "aint", "ain't", "not"]
    tokens = remove_noise(text, remove_punctuation=False,
                          remove_stop_word=False)
    negation_indices = [i for i, token in enumerate(
        tokens) if negation_words.__contains__(token.lower())]
    punctuation_indices = [i for i, token in enumerate(
        tokens) if punctuation.__contains__(token.lower())]
    mixed_indices = punctuation_indices
    mixed_indices.extend(negation_indices)
    postive_negative_context = __partition(tokens, __get_next(
        negation_indices, sorted(mixed_indices)))
    postitive_context = []
    negative_context = []

    for context in postive_negative_context:
        if len(set(context).intersection(negation_words)) == 0:
            postitive_context.append(context)
        else:
            negative_context.append(context)
    return postitive_context, negative_context,


def extract_ordered_contexts(text):
    text = text.lower()
    # p = Punctuator('resources/models/Demo-Europarl-EN.pcl')
    # text = (p.punctuate(text))
    punctuation = ['.', ',', ';', ':', ';', '!', '?', 'but','...','..','....']
    negation_words = ["n't", "never", "no", "nothing", "nowhere", "noone", "nonenot",
                      "havent", "haven't", "hasnt", "hasn't" "hadnt", "hadn't",
                      "cant", "can't", "couldnt", "couldn't", "shouldnt", "shouldn't",
                      "wont", "won't", "wouldnt", "wouldn't", "dont", "don't", "doesnt",
                      "doesn't", "didnt", "didn't", "isnt", "isn't", "arent", "aren't", "aint", "ain't", "not"]
    tokens = remove_noise(text, remove_punctuation=False,
                          remove_stop_word=False)
    negation_indices = [i for i, token in enumerate(
        tokens) if negation_words.__contains__(token.lower())]
    punctuation_indices = [i for i, token in enumerate(
        tokens) if punctuation.__contains__(token.lower())]
    mixed_indices = punctuation_indices
    mixed_indices.extend(negation_indices)
    postive_negative_context = __partition(tokens, __get_next(
        negation_indices, sorted(mixed_indices)))
    ordered_contexts = []

    for context in postive_negative_context:
        if len(set(context).intersection(negation_words)) == 0:
            ordered_contexts.append(('POS', context))
        else:
            ordered_contexts.append(('NEG', context))
    return ordered_contexts


if __name__ == "__main__":
   # create_index()
    print(extract_contexts('hi you are not my friend'))
    print(extract_ordered_contexts("Don't buy this piece of shit, it's the worst "))
