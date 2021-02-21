import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from gloover_model.classifier import Classifier
from gloover_model.db_manager import DbManager
from gloover_model.serialization.database.review import Review
from gloover_model.serialization.database.webpage import WebPage
from gloover_ws.blueprints.scraper_bp import scraper_api

application = Flask(__name__)
application.register_blueprint(scraper_api, url_prefix='/scraper')
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
    'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
classifier = Classifier(test_size=0.1, train_size=0.1)
mongo = PyMongo(application)
db = mongo.db

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
