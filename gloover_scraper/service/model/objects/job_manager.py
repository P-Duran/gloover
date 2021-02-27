import datetime

from apscheduler.job import Job

from .scrape_template import ScrapeTemplate
from ..utils.readers import read_items


class JobManager(object):
    def __init__(self):
        self._storage = {}

    def add_job(self, job: Job, scrape_template: ScrapeTemplate):
        if job.id not in self._storage:
            self._storage[job.id] = self.job_to_json(job, scrape_template)
            return True
        return False

    def get_job(self, job_id: str):
        return self._storage[job_id]

    def remove_job(self, job_id: str):
        del self._storage[job_id]

    def update_job_state(self, job_id: str, state: str):
        if state == 'finished':
            self._storage[job_id]['finish_time'] = datetime.datetime.now()
        self._storage[job_id]['state'] = state

    def get_jobs(self):
        for key in self._storage.keys():
            if 'file_path' in self._storage[key]:
                self._storage[key]['scraped_items'] = sum(1 for _ in open(self._storage[key]['file_path']))
        return self._storage

    @classmethod
    def job_to_json(cls, job: Job, scrape_template: ScrapeTemplate):
        return {
            "id": job.id,
            "name": job.name,
            "trigger": str(job.trigger),
            "next_run_time": str(job.next_run_time),
            "state": 'scheduled',
            "url": scrape_template.url,
            "max_requests": scrape_template.max_requests,
            "spider": scrape_template.spider,
            "file_path": scrape_template.file_path,
            "scraped_items": 0,
        }