import datetime
from typing import List

from apscheduler.job import Job

from .scrape_template import ScrapeTemplate


class JobManager(object):
    _DATETIME_FORMAT = "%d/%m/%Y, %H:%M:%S:%f"

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
        if job_id in self._storage:
            if state == 'finished':
                self._storage[job_id]['finish_time'] = datetime.datetime.now().strftime(self._DATETIME_FORMAT)
            self._storage[job_id]['state'] = state

    def get_jobs(self, jobs: List[Job]):
        for key in self._storage.keys():
            if 'next_run_time' in self._storage[key]:
                self._storage[key]['next_run_time'] = next(
                    (job.next_run_time.strftime(self._DATETIME_FORMAT) for job in jobs if job.id == key),
                    self._storage[key]['next_run_time'])
            if 'file_path' in self._storage[key]:
                try:
                    self._storage[key]['scraped_items'] = sum(1 for _ in open(self._storage[key]['file_path']))
                except Exception:
                    pass
        return self._storage

    @classmethod
    def job_to_json(cls, job: Job, scrape_template: ScrapeTemplate):
        trigger = str(job.trigger).split('[')
        trigger_type = trigger[0].strip()
        trigger_time = trigger[1].replace(']', "").strip()
        return {
            "id": job.id,
            "name": job.name,
            "trigger": trigger_type,
            "trigger_time": trigger_time,
            "next_run_time": job.next_run_time.strftime(cls._DATETIME_FORMAT),
            "state": 'scheduled',
            "url": scrape_template.url,
            "max_requests": scrape_template.max_requests,
            "spider": scrape_template.spider,
            "file_path": scrape_template.file_path,
            "scraped_items": 0,
        }
