from logging import DEBUG

from flask.app import Flask
from flask.globals import g, request
from flask.helpers import make_response
from flask.json import jsonify

from app.models.exceptions import Unauthorized, BadRequest, Forbidden
from app.views.tasks import tasks
from app.views.projects import projects

app = Flask(__name__, instance_relative_config=True)

app.logger.setLevel(DEBUG)

app.config.from_object('config.default')
# there are causing errors
# app.config.from_envvar('APP_CONFIG_FILE')
# app.config.from_pyfile('config.py')


@app.before_request
def options_autoreply():
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()
        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']
        h = resp.headers
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers
        return resp


@app.after_request
def set_allow_origin(resp):
    h = resp.headers
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Credentials'] = "false"
        h['Access-Control-Max-Age'] = "3600"
    return resp


app.register_blueprint(tasks, url_prefix='/api/tasks')
app.register_blueprint(projects, url_prefix='/api/project')


@app.errorhandler(404)
def handle_not_found(error):
    return make_response(jsonify({'message': 'Not Found'}), 404)


@app.errorhandler(500)
def handle_internal_server_error(error):
    return make_response(jsonify({'message': 'Internal Server Error'}), 500)


@app.errorhandler(BadRequest)
def handle_invalid_usage(error):
    return make_response(jsonify(error.to_dict()), error.status_code)


@app.errorhandler(Unauthorized)
def handle_invalid_usage(error):
    return make_response(jsonify(error.to_dict()), error.status_code)


@app.errorhandler(Forbidden)
def handle_invalid_usage(error):
    return make_response(jsonify(error.to_dict()), error.status_code)
