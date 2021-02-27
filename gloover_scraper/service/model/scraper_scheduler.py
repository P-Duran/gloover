import os
import sys
import time

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_SUBMITTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import JobEvent

from .objects.job_manager import JobManager
from .objects.scrape_template import ScrapeTemplate


class ScraperScheduler(object):
    def __init__(self):
        self._job_manager = JobManager()
        self._scheduler = BackgroundScheduler(daemon=True)
        self._scheduler.add_listener(self._executed_listener, EVENT_JOB_EXECUTED)
        self._scheduler.add_listener(self._submitted_listener, EVENT_JOB_SUBMITTED)
        self._scheduler.start()

    def add_scrape_interval(self, scrape_template: ScrapeTemplate, hours=100):
        job = self._scheduler.add_job(
            self._run_spider, args=scrape_template.generate_args_list(), id=scrape_template.scrape_id.__str__(),
            hours=hours)
        self._job_manager.add_job(job, scrape_template)
        return job

    def add_scrape_date(self, scrape_template: ScrapeTemplate, run_date):
        job = self._scheduler.add_job(
            self._run_spider, args=scrape_template.generate_args_list(), id=scrape_template.scrape_id.__str__(),
            run_date=run_date)
        self._job_manager.add_job(job, scrape_template)
        return job

    def add_test_interval(self):
        job = self._scheduler.add_job(self._test_function, trigger="interval", seconds=10)
        job2 = self._scheduler.add_job(self._test_function)
        self._job_manager.add_job(job, None)
        self._job_manager.add_job(job2, None)
        return job

    def get_jobs(self):
        return self._job_manager.get_jobs()

    def get_apscheduler_jobs(self):
        return self._scheduler.get_jobs()

    @classmethod
    def _run_spider(cls, spider, url, max_requests, file_path):
        os.system(f"""scrapy crawl {spider} -a url="{url}" -a max_requests={max_requests} -o {file_path}""")

    def _executed_listener(self, event: JobEvent):
        job = self._scheduler.get_job(event.job_id)
        if job and str(job.trigger).__contains__("interval"):
            state = "scheduled"
        else:
            state = "finished"
        self._job_manager.update_job_state(event.job_id, state)

    def _submitted_listener(self, event: JobEvent):
        self._job_manager.update_job_state(event.job_id, "running")

    @classmethod
    def _test_function(cls):
        time.sleep(5)
        print("TEST FUNCTION", file=sys.stderr)

