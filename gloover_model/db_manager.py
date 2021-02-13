from typing import List

import gloover_ws.app
from gloover_service.exceptions.document_already_exists_exception import DocumentAlreadyExistsException
from gloover_service.objects.database.review import Review
from gloover_service.objects.database.webpage import WebPage
from gloover_service.utils.logger import Logger


class DbManager:

    def add_reviews(self, reviews: List[Review], webpage: WebPage):
        if len(reviews) == 0:
            Logger.log_warning("The reviews are empty")
            return
        if not all([review.webpage == reviews[0].webpage for review in reviews]):
            raise Exception("The reviews are not from the same source")
        self.add_website(webpage)
        gloover_ws.app.db.reviews.insert_many([r.__dict__ for r in reviews])

    def add_website(self, webpage: WebPage):
        try:
            gloover_ws.app.db.websites.create_index([("name", -1)], unique=True)
            gloover_ws.app.db.websites.insert_one(webpage.__dict__)
        except Exception as e:
            raise DocumentAlreadyExistsException("Web page with name " + webpage.name + " already exists", e)
