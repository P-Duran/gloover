import os
import uuid


class ScrapeTemplate(object):
    def __init__(self, spider: str, url: str, max_requests: int):
        self.scrape_id = uuid.uuid4()
        self.max_requests = max_requests
        self.url = url
        self.spider = spider
        self.file_path = self._generate_file_path()

    def _generate_file_path(self):
        file_path = f"generated/{self.spider}/items-{self.scrape_id}.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        return file_path

    def generate_args_list(self):
        return [self.spider, self.url, self.max_requests, self.file_path]
