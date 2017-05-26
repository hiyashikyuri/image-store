from flask.blueprints import Blueprint
from flask.json import jsonify

from app.services import task_service

tasks = Blueprint('tasks', __name__)


@tasks.route('')
def find_all():
    return jsonify({
        "response": task_service.find_all()
    })


@tasks.route('/<task_uuid>')
def find_one(task_uuid):
    return jsonify({
        "response": task_service.find_one(task_uuid).to_dict()
    })
