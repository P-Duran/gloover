import time

from apscheduler.job import Job
from flask import Flask, jsonify, request, Response

from exceptions.gloover_scraper_exception import GlooverScraperException
from exceptions.null_request_args_exception import NullRequestArgsException
from service.model.objects.scrape_template import ScrapeTemplate
from service.scheduler_service import SchedulerService
from service.scraped_data_service import ScrapedDataService

application = Flask(__name__)
scheduler_service = SchedulerService(application.logger)
scraped_data_service = ScrapedDataService(application.logger)


@application.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    max_requests = request.form.get('max_requests')
    spider = request.form.get('spider_name')
    trigger = request.form.get('trigger')
    trigger_option = request.form.get('trigger_option')
    test = request.form.get('test', False)

    if not (url and max_requests and spider):
        raise NullRequestArgsException("url, max_requests or spider query params where null")

    scraper_template = ScrapeTemplate(spider, url, max_requests)
    job = scheduler_service.schedule_scraper(scraper_template, trigger, trigger_option, test)

    return jsonify(id=job.id, items=job_to_json(job))


@application.route('/jobs', methods=['GET'])
def jobs():
    stream = request.args.get('stream', False)

    def inner():
        while True:
            time.sleep(3)
            yield 'data: %s\n\n' % scheduler_service.get_jobs().__str__()

    if stream:
        return Response(inner(), mimetype="text/event-stream")
    else:
        return jsonify(jobs=scheduler_service.get_jobs(),
                       apscheduler_jobs=[job_to_json(j) for j in scheduler_service.get_apscheduler_jobs()])


@application.route('/jobs/<scraper_id>', methods=['DELETE'])
def cancel_job(scraper_id):
    scheduler_service.cancel_scraper(scraper_id)
    return jsonify(status='ok')


@application.route('/spiders', methods=['GET'])
def get_spiders():
    return jsonify(spiders=scheduler_service.get_system_spiders())


@application.route('/containers', methods=['GET'])
def get_containers():
    spider = request.args.get('spider_name')
    return jsonify(containers=scraped_data_service.get_containers(spider))


@application.route('/containers/<container_id>')
def get_items(container_id):
    limit = int(request.args.get('limit', 1000))
    page = int(request.args.get('page', 1))
    limited_items, pagination = scraped_data_service.get_container_items(container_id, limit=limit, page=page)
    return jsonify(items=limited_items, pagination=pagination)


@application.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, GlooverScraperException):
        return process_exception(e, 500), 500
    # now you're handling non-HTTP exceptions only
    return str(e)


@application.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header["Access-Control-Allow-Methods"] = "GET, POST, PATCH, PUT, DELETE, OPTIONS"
    return response


def process_exception(e: Exception, code: int):
    return jsonify(code=code, error=e.__dict__)


def job_to_json(job: Job):
    return {
        "name": job.name,
        "id": job.id,
        "trigger": str(job.trigger),
        "next_run_time": str(job.next_run_time)

    }
