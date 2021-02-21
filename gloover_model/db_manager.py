from typing import List

import gloover_ws.app
from gloover_model.exceptions.document_already_exists_exception import DocumentAlreadyExistsException
from gloover_model.serialization.database.review import Review
from gloover_model.serialization.database.webpage import WebPage
from gloover_service.utils.logger import Logger


class DbManager:
    @classmethod
    def add_reviews(cls, reviews: List[Review], webpage: WebPage):
        if len(reviews) == 0:
            Logger.log_warning("The reviews are empty")
            return
        if not all([review.domain == reviews[0].domain for review in reviews]):
            raise Exception("The reviews are not from the same source")
        try:
            cls.add_webpage(webpage)
        except DocumentAlreadyExistsException:
            Logger.log_warning("Webpage already exists")
        gloover_ws.app.db.reviews.insert_many([r.__dict__ for r in reviews])

    @classmethod
    def add_webpage(cls, webpage: WebPage):
        try:
            gloover_ws.app.db.websites.create_index([("company_name", -1)], unique=True)
            gloover_ws.app.db.websites.insert_one(webpage.__dict__)
        except Exception as e:
            raise DocumentAlreadyExistsException("""Web page with "company_name": """ + webpage.company_name + """" 
            already exists""", e)
