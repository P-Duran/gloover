import os
import sys
from datetime import datetime

import crochet
from flask import Flask, request
from flask import jsonify
from flask_pymongo import PyMongo
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings

from gloover_model.classifier import Classifier
from gloover_model.db_manager import DbManager
from gloover_model.scraper.spiders.amazon_spider import AmazonSpider
from gloover_service.objects.database.review import Review
from gloover_service.objects.database.webpage import WebPage

application = Flask(__name__)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
    'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
classifier = Classifier(test_size=0.1, train_size=0.1)
mongo = PyMongo(application)
db = mongo.db
s = get_project_settings
crochet.setup()

crawl_runner = CrawlerRunner()  # requires the Twisted reactor to run
output_data = []

runner = CrawlerRunner()
output = []
avaliable = True


@application.route('/crawl')
def crawl_url():
    global avaliable
    msg = 'Scraper starting'
    if avaliable:
        scrape_with_crochet()
        msg = 'Scraper scraping...'
        avaliable = False
    return jsonify(avaliable=msg)  # Returns the scraped data after being running for 20 seconds.


@application.route('/results')
def results():
    return jsonify(output_data=output_data)


@application.route('/state')
def state():
    return jsonify(avaliable=avaliable)


@crochet.run_in_reactor
def scrape_with_crochet():
    global runner
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = runner.crawl(AmazonSpider, max_iterations=1)
    eventual.addCallback(_spider_closed)
    return eventual


def _spider_closed(w):
    global avaliable
    avaliable = True


def _crawler_result(item, response, spider):
    global output_data
    output_data.append(dict(item))


@application.route('/analyze')
def hello():
    text = request.form['text']
    polarity = 'negative'
    classification = [1]
    # classifier.classify([text])
    if classification[0] == 1:
        polarity = 'positive'
    return '"' + text + '" is ' + polarity + str(classification)


@application.route('/database/reviews', methods=['GET'])
def get_reviews():
    _reviews = db.reviews.find()
    data = []
    print(_reviews, file=sys.stderr)
    for review in _reviews:
        del review['_id']
        data.append(review)
    return jsonify(
        status=True,
        data=data
    )


@application.route('/test')
def todo():
    try:
        db_manager = DbManager()
        db_manager.add_reviews([Review(product_name="product name", text="a text", user_name="user",
                                       date=datetime(2014, 1, 1, 0, 0),
                                       country="Spain", polarity=5, webpage="www.amazon.es")],
                               WebPage("amazon", "www.amazon.com", 5))
        return jsonify(
            status=True
        )
    except Exception as e:
        return jsonify(
            error="Could not get this",
            traceback=str(e)
        )


@application.route('/info', methods=['GET'])
def info():
    return jsonify(
        status=True,
        message='Server is running!'
    ), 201


@application.route('/todo', methods=['POST'])
def create_todo():
    data = request.get_json(force=True)
    item = {
        'todo': data['todo']
    }
    db.todo.insert_one(item)

    return jsonify(
        status=True,
        message='To-do saved successfully!'
    ), 201
