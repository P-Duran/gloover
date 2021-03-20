import os

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

from gloover_model.classifier import Classifier
from gloover_model.exceptions.gloover_exception import GlooverException
from gloover_ws.blueprints.database_bp import database_api
from gloover_ws.blueprints.scraper_bp import scraper_api

application = Flask(__name__)
application.register_blueprint(scraper_api, url_prefix='/scraper')
application.register_blueprint(database_api, url_prefix='/database')
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


@application.route('/info', methods=['GET'])
def info():
    return jsonify(
        status=True,
        message='Server is running!'
    ), 201


#@application.errorhandler(Exception)
def handle_exception(e: Exception):
    # pass through HTTP errors
    if isinstance(e, GlooverException):
        return process_exception(e, 500), 500
    # now you're handling non-HTTP exceptions only
    application.logger.error(e)
    return str(e)


@application.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header["Access-Control-Allow-Methods"] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
    return response


def process_exception(e: Exception, code: int):
    return jsonify(code=code, error=e.__dict__)
