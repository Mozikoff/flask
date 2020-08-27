from flask import (
    Blueprint, request, make_response, jsonify
)
from flaskmail.db import get_db
from flaskmail.utils import validate_json, validate_schema
from flaskmail.jsonschema import dictionary_schema

bp = Blueprint('dictionary', __name__)


@bp.route('/dictionary', methods=('POST', ))
@validate_json
@validate_schema(dictionary_schema)
def create():
    if request.method == 'POST':
        req_data = request.get_json()
        key = req_data['key']
        value = req_data['value']
        error = None

        dict_value = get_dictionary_value(key)

        if dict_value:
            return make_response(jsonify({"message": "Key already exist"}), 409)

        if not key:
            error = 'Key is required.'
        elif not value:
            error = 'Value is required.'

        if error is not None:
            return error
        else:
            db = get_db()
            db.execute(
                'INSERT INTO dictionary (key, value)'
                ' VALUES (?, ?)',
                (key, value)
            )
            db.commit()
        return make_response(jsonify({"message": "Dictionary value created"}), 201)


@bp.route('/dictionary/<key>', methods=('GET', ))
def get(key):
    dict_value = get_dictionary_value(key)

    if request.method == 'GET':
        if dict_value is None:
            return make_response(jsonify({"error": "Not found"}), 404)
        return make_response(jsonify({'key': key, "value": dict_value['value']}), 200)


@bp.route('/dictionary/<key>', methods=('PUT', ))
@validate_json
@validate_schema(dictionary_schema)
def update(key):
    dict_value = get_dictionary_value(key)

    if request.method == 'PUT':
        req_data = request.get_json()
        key = req_data['key']
        value = req_data['value']

        if dict_value is None:
            return make_response(jsonify({"error": "Not found"}), 404)
        else:
            db = get_db()
            db.execute(
                'UPDATE dictionary SET value = ?'
                'WHERE key = ?',
                (value, key)
            )
            db.commit()
        return make_response(jsonify({"message": "Dictionary value replaced"}), 201)


@bp.route('/dictionary/<key>', methods=('DELETE', ))
def delete(key):
    if request.method == 'DELETE':
        db = get_db()
        db.execute(
            'DELETE FROM dictionary'
            ' WHERE key = ?',
            key
        )
        db.commit()
        return make_response(jsonify({}), 204)


def get_dictionary_value(key):
    dict_value = get_db().execute(
        'SELECT key, value'
        ' FROM dictionary'
        ' WHERE key = ?',
        key
    ).fetchone()
    return dict_value
