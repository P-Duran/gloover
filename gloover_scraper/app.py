import datetime
import glob
import json
import os
import re
import subprocess
import uuid
from math import ceil

from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request

from exceptions.gloover_scraper_exception import GlooverScraperException
from exceptions.null_request_args_exception import NullRequestArgsException
from exceptions.unable_to_read_data_exception import UnableToReadDataException

application = Flask(__name__)
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()
_ID_FILE_REGEX = "([^/]+/)*((?P<spider>[^/]+)/)+items-(?P<id>[^/]+).json"


@application.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    max_requests = request.form.get('max_requests')
    spider = request.form.get('spider_name')
    trigger = request.form.get('trigger')

    scraping_id = uuid.uuid4()
    file_name_path = f"generated/{spider}/items-{scraping_id}.json"
    if not (url and max_requests and spider):
        raise NullRequestArgsException("url, max_requests or spider query params where null")

    os.makedirs(os.path.dirname(file_name_path), exist_ok=True)
    if trigger == 'date':
        run_date = request.form.get('run_date')
        job = scheduler.add_job(
            run_spider, args=[spider, url, max_requests, file_name_path], id=scraping_id.__str__(), run_date=run_date)
    elif trigger == 'interval':
        hours = request.form.get('hours')
        job = scheduler.add_job(
            run_spider, args=[spider, url, max_requests, file_name_path], id=scraping_id.__str__(), hours=hours)
    elif trigger == 'test':
        job = scheduler.add_job(sensor, id=scraping_id.__str__(), trigger="interval", seconds=3)
    else:
        job = scheduler.add_job(
            run_spider, args=[spider, url, max_requests, file_name_path], id=scraping_id.__str__())
    return jsonify(id=scraping_id, items=job_to_json(job))


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
            try:
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file))
            except OSError:
                mtime = datetime.datetime.fromtimestamp(0)
            if file_spider not in result:
                result[file_spider] = {}
            result[file_spider][file_id] = {"id": file_id, "spider": file_spider, "path": file,
                                            "last_modified": str(mtime)}
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
        application.logger.error(UnableToReadDataException(e, "Unable to load the data from: " + file_path))
        return []


@application.route("/job", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        job = scheduler.add_job(sensor, trigger="interval", seconds=3)
        return jsonify(job=job_to_json(job))
    elif request.method == 'GET':
        return jsonify(jobs=[job_to_json(job) for job in scheduler.get_jobs()])
    return "Welcome Home :) !"


@application.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, GlooverScraperException):
        return process_exception(e, 500), 500
    # now you're handling non-HTTP exceptions only
    return e


def process_exception(e: Exception, code: int):
    return jsonify(code=code, error=e.__dict__)


def run_spider(spider, url, max_requests, file_name_path):
    os.system(f"""scrapy crawl {spider} -a url="{url}" -a max_requests={max_requests} -o {file_name_path}""")


def job_to_json(job: Job):
    return {
        "name": job.name,
        "id": job.id,
        "trigger": str(job.trigger),
        "next_run_time": str(job.next_run_time)

    }


def sensor():
    """ Function for test purposes. """
    application.logger.debug(datetime.datetime.now())