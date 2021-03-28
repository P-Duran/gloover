from flask import Blueprint, request, jsonify

from gloover_model.exceptions.null_request_args_exception import NullRequestArgsException
from gloover_service.classifier_service import ClassifierService

classifier_api = Blueprint('classifier_api', __name__)
classifier_service = ClassifierService()


@classifier_api.route('/classify', methods=['PUT'])
def classify():
    text = request.form.get('text')
    if text is None:
        raise NullRequestArgsException("text was null")
    res = classifier_service.classify([text]).tolist()
    return jsonify(data={"text": text, "polarity": res[0]})


@classifier_api.route('/models')
def get_models():
    limit = request.args.get('limit', None)
    models = classifier_service.get_saved_models(limit)
    return jsonify(data=models)


@classifier_api.route('/models', methods=['POST'])
def add_model():
    model_id = request.form.get('asin', None)
    model_id, accuracy = classifier_service.create_model_from_database(model_id)
    return jsonify(data={"model_id": model_id, "accuracy": accuracy})


@classifier_api.route('/models/<id>', methods=['DELETE'])
def remove_model(id):
    res = classifier_service.remove_model(id)
    return jsonify(data=res)


@classifier_api.route('/models/<id>', methods=['PUT'])
def load_model(id):
    res = classifier_service.load_model(id)
    return jsonify(data=res)


@classifier_api.route('/models/current', methods=['GET'])
def get_current_model():
    return jsonify(data=classifier_service.get_current_model())
