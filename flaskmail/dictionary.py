from flask import (
    Blueprint, request, make_response, jsonify
)
from flaskmail.db import get_db
from flaskmail.utils import validate_json, validate_schema
from flaskmail.jsonschema import dictionary_schema
from datetime import datetime

bp = Blueprint('dictionary', __name__)


@bp.route('/dictionary', methods=('POST', ))
@validate_json
@validate_schema(dictionary_schema)
def create():
    if request.method == 'POST':
        req_data = request.get_json()
        key = req_data['key']
        value = req_data['value']
        dict_value = get_dictionary_value(key)

        if dict_value:
            return make_response(jsonify(result="Key already exist", time=datetime.now()), 409)

        db = get_db()
        db.execute(
            'INSERT INTO dictionary (key, value)'
            ' VALUES (?, ?)',
            (key, value)
        )
        db.commit()
        return make_response(jsonify(result=value, time=datetime.now()), 201)


@bp.route('/dictionary/<key>', methods=('GET', ))
def get(key):
    dict_value = get_dictionary_value(key)
    if request.method == 'GET':
        if dict_value is None:
            return make_response(jsonify(result="Not found", time=datetime.now()), 404)
        return make_response(jsonify(result=dict_value['value'], time=datetime.now()), 200)


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
            return make_response(jsonify(result="Not found", time=datetime.now()), 404)
        else:
            db = get_db()
            db.execute(
                'UPDATE dictionary SET value = ?'
                'WHERE key = ?',
                (value, key)
            )
            db.commit()
        return make_response(jsonify(result=value, time=datetime.now()), 201)


@bp.route('/dictionary/<key>', methods=('DELETE', ))
def delete(key):
    if request.method == 'DELETE':
        db = get_db()
        db.execute(
            'DELETE FROM dictionary'
            ' WHERE key = ?',
            (key, )
        )
        db.commit()
        return make_response(jsonify(result="null", time=datetime.now()), 200)


def get_dictionary_value(key):
    dict_value = get_db().execute(
        'SELECT key, value'
        ' FROM dictionary'
        ' WHERE key = ?',
        (key, )
    ).fetchone()
    return dict_value
