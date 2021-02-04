import time
import redis
from flask import Flask
import pandas as pd
import os
from gloover_model.classifier import Classifier

application = Flask(__name__)
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


@application.route('/<text>')
def hello(text):
    polarity = 'negative'
    classification = classifier.classify(pd.Series([text]))
    if classification[0] == 1:
        polarity = 'positive'
    return '"' + text + '" is ' + polarity + str(classification)

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)