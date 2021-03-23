from typing import List

from gloover_model.classifier import Classifier
from gloover_model.db_manager import DbManager
from gloover_service.utils.logger import Logger

classifier = Classifier()


class ClassifierService:
    def __init__(self):
        if classifier.model is None:
            self._initialize_classifier()

    def classify(self, texts: List[str]):
        return classifier.classify(texts)

    def create_model_from_database(self, asin):
        reviews = DbManager.get_reviews(limit=5000)
        model_id, accuracy = classifier.create_model(reviews, model_id=asin)
        return model_id, accuracy

    @classmethod
    def _initialize_classifier(cls):
        Logger.log_warning("initializing Classifier...")
        if not classifier.load_first_model():
            reviews = DbManager.get_reviews(limit=5000)
            model_id, accuracy = classifier.create_model(reviews)
            Logger.log_warning(model_id + "::" + accuracy)
