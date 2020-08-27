from flask import (
    jsonify,
    request,
)
from functools import wraps

from werkzeug.exceptions import BadRequest
from werkzeug.routing import ValidationError
from jsonschema import validate


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.get_json()
        except BadRequest:
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        return f(*args, **kw)
    return wrapper


def validate_schema(json_schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.get_json(), json_schema)
            except ValidationError as e:
                return jsonify({"error": e.message}), 400
            return f(*args, **kw)
        return wrapper
    return decorator
