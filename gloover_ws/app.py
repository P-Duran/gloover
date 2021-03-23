import logging
import os

from flask import Flask, jsonify
from flask_pymongo import PyMongo

from gloover_model.exceptions.gloover_exception import GlooverException
from gloover_ws.blueprints.classifier_bp import classifier_api
from gloover_ws.blueprints.database_bp import database_api
from gloover_ws.blueprints.scraper_bp import scraper_api

logging.basicConfig(filename='gloover.log', level=logging.WARNING)
application = Flask(__name__)
application.register_blueprint(classifier_api, url_prefix='/classifier')
application.register_blueprint(scraper_api, url_prefix='/scraper')
application.register_blueprint(database_api, url_prefix='/database')

application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ[
    'MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
mongo = PyMongo(application)
db = mongo.db


@application.route('/info', methods=['GET'])
def info():
    return jsonify(
        status=True,
        message='Server is running!'
    ), 201


# @application.errorhandler(Exception)
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
