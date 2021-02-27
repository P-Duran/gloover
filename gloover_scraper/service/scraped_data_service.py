import datetime
import glob
import json
import os
import re
from math import ceil

from .model.utils.readers import read_items


class ScrapedDataService(object):
    _ID_FILE_REGEX = "([^/]+/)*((?P<spider>[^/]+)/)+items-(?P<id>[^/]+).json"

    def __init__(self, logger):
        self.logger = logger

    def get_container_items(self, container_id: str, limit: int, page: int):
        file_path = None
        for file in glob.glob('generated/**/*.json'):
            if file.endswith("items-" + container_id + ".json"):
                file_path = file
        items = read_items(file_path)
        limited_items = items[limit * (page - 1):limit * page]
        pagination = {"page": page, "last_page": ceil(len(items) / limit), "limit": limit,
                      "page_items": len(limited_items),
                      "total_items": len(items)}
        return limited_items, pagination

    def get_containers(self, spider: str = None):
        glob_regex = f"generated/{spider}/*.json"
        if not spider:
            glob_regex = "generated/**/*.json"
        result = {}
        for file in glob.glob(glob_regex):
            file_match = re.search(self._ID_FILE_REGEX, file)
            if file_match:
                file_id = file_match.group("id")
                file_spider = file_match.group("spider")
                try:
                    las_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file))
                except OSError:
                    las_modified = datetime.datetime.fromtimestamp(0)
                if file_spider not in result:
                    result[file_spider] = {}
                result[file_spider][file_id] = {"id": file_id, "spider": file_spider, "path": file,
                                                "last_modified": str(las_modified)}
        return result


