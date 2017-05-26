from functools import wraps

from flask.globals import request

from app.models.exceptions import Unauthorized


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization = request.headers.get('Authorization', None)
        if authorization is None:
            raise Unauthorized('Unauthorized')
        # TODO check that the authorization token is valid and get the user info
        return f(*args, **kwargs)

    return decorated_function
