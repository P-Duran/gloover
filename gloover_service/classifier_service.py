import glob
import pathlib
import re
from typing import List

from gloover_model.classifier import Classifier
from gloover_model.db_manager import DbManager
from gloover_model.singleton.singleton_meta import SingletonMeta
from gloover_service.utils.logger import Logger


class ClassifierService(metaclass=SingletonMeta):
    _MODEL_REGEX = "([^/]+/)*(?P<id>[^/]+).mdl"
    _MODELS_DIR = "resources/models"
    _MODEL_CONTAINER_REGEX = _MODELS_DIR + "/*.mdl"

    def __init__(self):
        self.classifier = Classifier()
        if self.classifier.model is None:
            self._initialize_classifier()

    def classify(self, texts: List[str]):
        return self.classifier.classify(texts)

    def get_current_model(self):
        return self.classifier.model_id

    def create_model_from_database(self, model_id):
        reviews = DbManager.get_reviews(limit=5000)
        model_id, accuracy = self.classifier.create_model(reviews, model_id=model_id)
        return model_id, accuracy

    def load_model(self, model_id):
        return self.classifier.load_model(model_id)

    def remove_model(self, model_id):
        file_to_rem = pathlib.Path(self._MODELS_DIR + "/" + model_id + ".mdl")
        if file_to_rem.is_file():
            file_to_rem.unlink()
            return "ok"
        else:
            raise Exception("The model with id '" + model_id + "' does not exist")

    def get_saved_models(self, limit=None):
        model_ids = []
        retrieved = 0
        for file in glob.glob(self._MODEL_CONTAINER_REGEX):
            if limit is not None and retrieved >= limit:
                return model_ids
            file_match = re.search(self._MODEL_REGEX, file)
            model_id = file_match.group("id")
            model_ids.append(model_id)
            retrieved += 1
        return model_ids

    def get_last_model(self):
        model = self.get_saved_models(1)
        if len(model) > 0:
            return model[0]
        else:
            return None

    def _initialize_classifier(self):
        Logger.log_warning("initializing Classifier...")
        model = self.get_last_model()
        if model is None:
            reviews = DbManager.get_reviews(limit=5000)
            model_id, accuracy = self.classifier.create_model(reviews)
            self.classifier.load_model(model_id)
            Logger.log_warning(model_id + "::" + accuracy)
        else:
            self.classifier.load_model(model)
