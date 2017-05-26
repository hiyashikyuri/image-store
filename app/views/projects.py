from flask.blueprints import Blueprint
from flask.json import jsonify

from app.services import project_service

projects = Blueprint('projects', __name__)


@projects.route('')
def find_all():
    return jsonify({
        "response": project_service.find_all()
    })


@projects.route('/<task_uuid>')
def find_one(task_uuid):
    return jsonify({
        "response": project_service.find_one(task_uuid).to_dict()
    })
