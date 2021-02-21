import json
import os

from flask import Flask, jsonify, request

application = Flask(__name__)


@application.route('/scrape')
def scrape():
    url = request.args.get('url')
    max_requests = request.args.get('max_requests')
    spider = request.args.get('spider_name')
    os.system(f"""scrapy crawl {spider} -a url="{url}" -a max_requests={max_requests} -o items.json""")
    return jsonify(data=read_items())


@application.route('/data')
def get_data():
    return jsonify(data=read_items())


def read_items():
    with open('items.json') as json_file:
        return json.load(json_file)
