from flask import Blueprint, request, jsonify

from gloover_model.exceptions.request_args_exception import RequestArgsException
from gloover_service.classifier_service import ClassifierService

classifier_api = Blueprint('classifier_api', __name__)
classifier_service = ClassifierService()


@classifier_api.route('/classify', methods=['PUT'])
def classify():
    text = request.form.get('text')
    if text is None:
        raise RequestArgsException("text was null")
    res = classifier_service.classify([text]).tolist()
    return jsonify(data={"text": text, "polarity": res[0]}, model_id=classifier_service.get_current_model())


@classifier_api.route('/models')
def get_models():
    limit = request.args.get('limit', None)
    models = classifier_service.get_saved_models(limit)
    return jsonify(data=models)


@classifier_api.route('/models', methods=['POST'])
def add_model():
    model_id = request.form.get('asin', None)
    source = request.form.get('source', 'database')
    if source == 'database':
        model_id, accuracy = classifier_service.create_model_from_database(model_id)
    else:
        model_id, accuracy = classifier_service.create_model_from_file()
    return jsonify(data={"model_id": model_id, "accuracy": accuracy}, model_id=classifier_service.get_current_model())


@classifier_api.route('/models/<id>', methods=['DELETE'])
def remove_model(id):
    res = classifier_service.remove_model(id)
    return jsonify(data=res, model_id=classifier_service.get_current_model())


@classifier_api.route('/models/<id>', methods=['PUT'])
def load_model(id):
    res = classifier_service.load_model(id)
    return jsonify(data=res)


@classifier_api.route('/models/<id>/test', methods=['GET'])
def test_model(id):
    asin = request.args.get('asin', None)
    res = classifier_service.test_model(id, asin)
    return jsonify(data=res)


@classifier_api.route('/models/current', methods=['GET'])
def get_current_model():
    return jsonify(data=classifier_service.get_current_model())
