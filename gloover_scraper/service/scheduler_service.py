import subprocess

from .model.scraper_scheduler import ScraperScheduler


class SchedulerService(object):

    def __init__(self, logger):
        self.logger = logger
        self._scheduler = ScraperScheduler()

    def schedule_scraper(self, scrape_template, trigger, time_option, test=False):
        if test:
            return self._scheduler.add_test_interval()
        else:
            if trigger == 'date':
                return self._scheduler.add_scrape_date(scrape_template, time_option)
            elif trigger == 'interval':
                return self._scheduler.add_scrape_interval(scrape_template, time_option)

    @classmethod
    def get_system_spiders(cls):
        result = subprocess.run(['scrapy', 'list'], stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")
        return [spider for spider in result if spider != ""]

    def get_jobs(self):
        return self._scheduler.get_jobs()

    def get_apscheduler_jobs(self):
        return self._scheduler.get_apscheduler_jobs()