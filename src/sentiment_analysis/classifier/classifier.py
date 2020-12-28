

import pandas as pd
from sklearn.svm import LinearSVC
from matplotlib import pyplot as plt
from mlxtend.plotting import plot_decision_regions
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split
import sklearn
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.pipeline import FeatureUnion, Pipeline
from sentiment_analysis.classifier.features.features import NegateWordsContext, PercentageContextNegative, PosTagCounter, TotalSentimentScore, WordsExtractor
from sklearn.metrics import f1_score, precision_score, recall_score

if __name__ == "__main__":
    data = pd.read_json(
        'resources/datasets/reviews_Cell_Phones_and_Accessories_5.json', lines=True)
    data.columns = ['asin', 'helpful', 'polarity', 'text', 'reviewTime', 'reviewerID',
                    'reviewerName', 'summary', 'unixReviewTime']
    data.polarity[data.polarity < 2.5] = -1
    data.polarity[data.polarity >= 2.5] = 1

    data = data[(data.polarity == 1) | (data.polarity == -1)]
    # data = pd.read_csv(
    #     'resources/datasets/Reddit_Data.csv', encoding="utf-8")
    # data.columns = ['text', 'polarity']
    # data = data[data.polarity != 0]
    labels = data.groupby('polarity').text.unique()
    # Sort the over-represented class to the head.
    labels = labels[labels.apply(len).sort_values(ascending=False).index]
    excess = len(labels.iloc[0]) - len(labels.iloc[1])
    remove = np.random.choice(labels.iloc[0], excess, replace=False)
    df2 = data[~data.text.isin(remove)]
    print(df2.polarity.value_counts())

    data_len = len(data)
    ppl_neg = Pipeline([('_NEG words', NegateWordsContext()),
                        ('word_ngrams', CountVectorizer(ngram_range=(1, 4), analyzer='word')), ])
    ppl = Pipeline([
        ('text_features', FeatureUnion([
            ('postag', PosTagCounter()),
            # ('v', Pipeline(
            #     [('efe', WordsExtractor()), ('ge', CountVectorizer(ngram_range=(1, 4), analyzer='char'))])),
            ('char_ngrams', CountVectorizer(ngram_range=(1, 4), analyzer='char')),
            ('neg', ppl_neg),
            ('tfidf', TfidfVectorizer()),
            ('%', PercentageContextNegative()),
            ('ss', TotalSentimentScore()),

        ])),
        ('clf',   MLPClassifier(hidden_layer_sizes=(100, 100, 100), max_iter=500, alpha=0.0001,
                     solver='sgd', verbose=10,  random_state=21, tol=0.000000001))
    ])

    data_train, data_test, y_train, y_true=train_test_split(
        df2['text'], df2['polarity'], test_size=0.1, train_size=0.1)
    model=ppl.fit(data_train, y_train)
    y_test=model.predict(data_test)
    print(y_test)
    newvals=pd.Series([
                        "Don't buy this piece of shit, it's the worst ",
                        "Way overpriced. Joycons are flimsy. Standard Switch is $300 and yet it can only be bought for $500. Nintendo get your act together. ",
                        "Terrible purchase. Not usually this critical but I’m very surprised that this is even a real product and that a manufacturer can even pass this as able to sell. Took 3 times to just get past the set up, kept getting frozen and had to reset it. Screen was blurry and had a strange glare. Seemed like it was going to break at anytime. Poor product",
                        "Bought brand new, arrived and when plugged in and turned on, screen had a bright spot. Now there is a second bright spot- both spots are getting brighter and spreading, and the computer is glitchy. Amazon gave me 100- off, they weren't a fan of exchanging... So I bought a POS computer for 400- after discount of 100- and now it is malfunctioning... Riiiiight. Not the best customer service on this one. I'm not very happy. I'm a 40 year old mother back in full time college. Nobody has touched the screen. We JUST got it delivered yesterday at 215pm... Has not even been 24 hours. This is awful",
                        "For those wondering if this great little laptop will take 16GB of DDR4 RAM, the answer is it sure will! I just successfully updated mine I bought back in late February with this DD4 module I just received earlier - Corsair Vengeance SODIMM 16GB (1x16GB) DDR4 2400Mhz C16 https://www.amazon.com/gp/product/B077S17RPZ/ I dual boot mine with Windows 10 and Linux (Pop!_OS 20.04) and in both I have 13.8GB total since 2GB are dedicated to the GPU. BTW there's only 1 RAM memory slot on this board and the one that came with this laptop is 8GB which means all 8GB are on this module NOT soldered on the board like it says in the Asus documentation. Just thought I'd make this helpful info public since I was looking for someone to confirm this before making my purchase but just went for it so you're welcome. :) ",
                        "This is a sleek and modern laptop! It barely takes any effort to type. I really like the backlit keyboard as well as the number keypad on the right. There are plenty of ports, HDMI and USB. The screen appears large for a compact laptop and the resolution is amazing. I work with a lot of photos and they look absolutely great! I appreciate the 8 GB of RAM which makes using Photoshop and other programs fast and efficient. This machine is quick to turn on and seems to last a long time on a battery charge. It is very lightweight and will be easy to travel with. I think this is an excellent value! The only thing I had to get used to is that the power button is in the upper right corner where my delete key was on my old computer, so I've had to relearn the placement of some of the keys. I highly recommend this computer! ",
                        "out of the box, this is a beautiful laptop. I felt how light it was and I thought to myself, there's no way I can get performance out of this thing. Turned it on and set up and the first thing I did was download World of Warcraft. It downloaded fast. It runs at about medium settings out of the box. I upgraded the SSD to a 900gb and put another stick of ram in and I can run *WoW* on high settings! Load screens zip by. I also tested on call of duty and fortnite and everything ran smoothly. This is the best bang for your buck, in my opinion. Put $100 into it and it's a beast! The screen is very clear as well and is very hd. The keys light up like a gaming computer and makes it easy to see the keys. The only downside to this laptop is the keyboard. I took some pictures of it. It's the number pad and the enter key. It's not a full number pad or enter key. Sometimes I hit the wrong keys due to this. It's minor, I'll be gaming on a different keyboard anyways! Enjoy!!! Buy it and don't look back! ",
                        "Good entry level laptop. Latest gen ryzen picasso at the time of this review. Good for basic functions at this price point. Comes with m.2 128 gb drive with room for another SSD.Win 10 is a giant pain in the rear, particularly S mode, which can be opted out of.",
                        "This laptop is a fantastic deal for the price. The laptop uses the same body as the $500+ Acer Aspire 5 models which is to say it is a fantastic body that is light and compact and very portable. Ram can easily be upgraded and adding a 2.5 SSD allows for additional memory over the 128gb included on the computer. The keyboard is comfortable to type on and as a bonus still includes a full numpad even if it is a bit cramped. The screen is a solid IPS screen and when you consider the price tag is amazing and beats a lot of the more expensive laptop screens I have seen. ",
                        "It freezes while you are using it. It does not support games ",
                        "Just abominable, at the absolute worst time in my life possible... Things kept not working, I kept calling customer service, barely intelligible robotic people kept telling me I needed to reset the hard drive and wipe out everything I'd put on it (again). Final straw was the touchpad suddenly stopped working - after an agonizing 2 hours on the phone, conclusion was a hardware problem, no choice but to return it. Also, the sound is WAY too soft - I tried all these fixes I found online, nothing helped. Why would you need fixes for something so basic as acceptable sound in 2019?? Went to Best Buy, the dude just winced when I told him I had bought an Acer. DO NOT BUY. I hardly ever bother to review products one way or the other, but I owe this one to you.",
                        "We purchased this product for my son’s birthday. As he starts playing with it, we realize it’s in safe mode and he’s not able to download or open the products he wants to use. Microsoft says it’s a glitch in their system and we need to wait for them to work it out. Amazon says they will replace with another unit, but they can’t guarantee that unit won’t have the same issue. So, here we are with a brand new computer, unused. Huge let down. Disappointing product with disappointing options to make it right",
                        "BUYER BE AWARE: This computer has Microsoft 10S. This is scam software by Microsoft to force you to use only Microsoft apps from their deserted island wasteland of an app store. The computer will not allow you to do anything else. You can upgrade to a full version of Microsoft 10... for another $134. Hard pass. STAY AWAY from ALL computers with Microsoft 10S!! Absolute garbage software. "]
                        )
    result=model.predict(newvals)
    print(sklearn.metrics.accuracy_score([-1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1],
                                         result))
    print(sklearn.metrics.accuracy_score(y_true, y_test))
    print(f1_score(y_test, y_true, average="macro"))
    print(precision_score(y_test, y_true, average="macro"))
    print(recall_score(y_test, y_true, average="macro"))
    # plot_decision_regions(X=X.values,
    #                       y=y.values,
    #                       clf=m1,
    #                       legend=2)

    # Update plot object with X/Y axis labels and Figure Titl
    # plt.xlabel(X.columns[0], size=14)
    # plt.title('SVM Decision Region Boundary', size=16)
