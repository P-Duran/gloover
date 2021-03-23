from flask import Blueprint, request, jsonify

from gloover_model.exceptions.null_request_args_exception import NullRequestArgsException
from gloover_service.classifier_service import ClassifierService

classifier_api = Blueprint('classifier_api', __name__)
classifier_service = ClassifierService()


@classifier_api.route('/classify')
def classify():
    text = request.form.get('text')
    if text is None:
        raise NullRequestArgsException("text was null")
    res = classifier_service.classify([text]).tolist()
    return jsonify(data=res)
