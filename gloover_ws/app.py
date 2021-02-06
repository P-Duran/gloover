
from flask import Flask, request, jsonify
import os
from flask_pymongo import PyMongo
from gloover_model.classifier import Classifier

application = Flask(__name__)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
classifier = Classifier(test_size=0.1, train_size=0.1)
mongo = PyMongo(application)
db = mongo.db


@application.route('/analyze')
def hello():
    text = request.form['text']
    polarity = 'negative'
    classification = classifier.classify([text])
    if classification[0] == 1:
        polarity = 'positive'
    return '"' + text + '" is ' + polarity + str(classification)
@application.route('/todo')
def todo():
    _todos = db.todo.find()

    item = {}
    data = []
    for todo in _todos:
        item = {
            'id': str(todo['_id']),
            'todo': todo['todo']
        }
        data.append(item)

    return jsonify(
        status=True,
        data=data
    )

@application.route('/todo', methods=['POST'])
def createTodo():
    data = request.get_json(force=True)
    item = {
        'todo': data['todo']
    }
    db.todo.insert_one(item)

    return jsonify(
        status=True,
        message='To-do saved successfully!'
    ), 201


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)