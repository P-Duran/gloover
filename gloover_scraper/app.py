import json
import os
from http.client import HTTPException

from flask import Flask, jsonify, request

from exceptions.null_request_args_exception import NullRequestArgsException
from exceptions.unable_to_read_data_exception import UnableToReadDataException

application = Flask(__name__)


@application.route('/scrape')
def scrape():
    url = request.args.get('url')
    max_requests = request.args.get('max_requests')
    spider = request.args.get('spider_name')
    if not (url and max_requests and spider):
        raise NullRequestArgsException("url, max_requests or spider query params where null")

    os.system(f"""scrapy crawl {spider} -a url="{url}" -a max_requests={max_requests} -o items.json""")
    return jsonify(data=read_items())


@application.route('/data')
def get_data():
    return jsonify(data=read_items())


def read_items():
    try:
        json_file = open('items.json')
        return json.load(json_file)
    except Exception as e:
        raise UnableToReadDataException(e, "Unable to load the data")


@application.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e
    # now you're handling non-HTTP exceptions only
    return process_exception(e, 500), 500


def process_exception(e: Exception, code: int):
    return jsonify(code=code, error=e.__dict__)