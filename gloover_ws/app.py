import time
import redis
from flask import Flask
import pandas as pd
from gloover_model.classifier import Classifier

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
classifier = Classifier(test_size=0.1, train_size=0.1)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/<text>')
def hello(text):
    polarity = 'negative'
    classification = classifier.classify(pd.Series([text]))
    if classification[0] == 1:
        polarity = 'positive'
    return '"' + text + '" is ' + polarity + str(classification)
