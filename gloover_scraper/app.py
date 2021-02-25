import glob
import json
import os
import re
import subprocess
import uuid
from math import ceil

from flask import Flask, jsonify, request

from exceptions.gloover_scraper_exception import GlooverScraperException
from exceptions.null_request_args_exception import NullRequestArgsException
from exceptions.unable_to_read_data_exception import UnableToReadDataException

application = Flask(__name__)

_ID_FILE_REGEX = "([^/]+/)*((?P<spider>[^/]+)/)+items-(?P<id>[^/]+).json"


@application.route('/scrape')
def scrape():
    url = request.args.get('url')
    max_requests = request.args.get('max_requests')
    spider = request.args.get('spider_name')
    file_id = uuid.uuid4()
    file_name_path = f"generated/{spider}/items-{file_id}.json"
    if not (url and max_requests and spider):
        raise NullRequestArgsException("url, max_requests or spider query params where null")

    os.makedirs(os.path.dirname(file_name_path), exist_ok=True)
    os.system(f"""scrapy crawl {spider} -a url="{url}" -a max_requests={max_requests} -o {file_name_path}""")
    return jsonify(id=file_id, items=read_items(file_name_path))


@application.route('/spiders')
def get_spiders():
    result = subprocess.run(['scrapy', 'list'], stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")
    return jsonify(spiders=[spider for spider in result if spider != ""])


@application.route('/container')
def get_containers():
    spider = request.args.get('spider_name')
    glob_regex = f"generated/{spider}/*.json"
    if not spider:
        glob_regex = "generated/**/*.json"
    result = {}
    for file in glob.glob(glob_regex):
        file_match = re.search(_ID_FILE_REGEX, file)
        if file_match:
            file_id = file_match.group("id")
            file_spider = file_match.group("spider")
            if file_spider not in result:
                result[file_spider] = {}
            result[file_spider][file_id] = {"id": file_id, "spider": file_spider, "path": file}
    return jsonify(containers=result)


@application.route('/container/<container_id>')
def get_items(container_id):
    limit = int(request.args.get('limit', 1000))
    page = int(request.args.get('page', 1))
    file_path = None
    for file in glob.glob('generated/**/*.json'):
        if file.endswith("items-" + container_id + ".json"):
            file_path = file
    items = read_items(file_path)
    limited_items = items[limit * (page - 1):limit * page]
    pagination = {"page": page, "last_page": ceil(len(items) / limit), "limit": limit, "page_items": len(limited_items),
                  "total_items": len(items)}
    return jsonify(items=limited_items, pagination=pagination)


def read_items(file_path):
    try:
        json_file = open(file_path)
        return json.load(json_file)
    except Exception as e:
        raise UnableToReadDataException(e, "Unable to load the data from: " + file_path)


@application.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, GlooverScraperException):
        return process_exception(e, 500), 500
    # now you're handling non-HTTP exceptions only
    return e


def process_exception(e: Exception, code: int):
    application.logger.error(e)
    return jsonify(code=code, error=e.__dict__)
