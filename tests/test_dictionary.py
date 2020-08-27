import pytest
import json
from flaskmail.db import get_db
from jsonschema import ValidationError

def test_create(client, app):
    with app.app_context():
        response = client.post(
            '/dictionary',
            data=json.dumps(dict(key='key3', value='value3')),
            content_type='application/json'
        )
        assert response.status_code == 201
        row = get_db().execute(
            "select * from dictionary where key = 'key3'",
        ).fetchone()
        assert row is not None
        assert row['value'] == 'value3'


def test_create_already_exist(client, app):
    with app.app_context():
        response = client.post(
            '/dictionary',
            data=json.dumps(dict(key='mail.ru', value='target')),
            content_type='application/json'
        )
        assert response.status_code == 409
        row = get_db().execute(
            "select count(1) from dictionary where key = 'mail.ru'",
        ).fetchone()
        assert row is not None
        assert row[0] == 1


@pytest.mark.parametrize(('data', 'message'), (
    ({}, b"'key' is a required property"),
    ({"key": "1"}, b"'value' is a required property"),
    ({"key": "5", "value": "bla bla", "another": "one"},
     b"Additional properties are not allowed ('another' was unexpected)"),
    ("test", b"payload must be a valid json"),
))
def test_create_validate_input(client, data, message):
    with pytest.raises(ValidationError):
        response = client.post('/dictionary',
                               data=json.dumps(data),
                               content_type='application/json')
        assert message in response.data


def test_get(client):
    response = client.get('/dictionary/mail.ru')
    assert response.status_code == 200
    assert b"target" in response.data


def test_get_not_found(client):
    response = client.get('/dictionary/foo')
    assert response.status_code == 404
    assert b"Not found" in response.data


def test_update(client, app):
    with app.app_context():
        response = client.put(
            '/dictionary/test_key',
            data=json.dumps(dict(key='test_key', value='replaced')),
            content_type='application/json'
        )
        assert response.status_code == 201
        row = get_db().execute(
            "select * from dictionary where key = 'test_key'",
        ).fetchone()
        assert row is not None
        assert row['value'] == 'replaced'


def test_update_not_found(client, app):
    with app.app_context():
        response = client.put(
            '/dictionary/some_random_key',
            data=json.dumps(dict(key='some_random_key', value='random_value')),
            content_type='application/json'
        )
        assert response.status_code == 404
        row = get_db().execute(
            "select * from dictionary where key = 'some_random_key'",
        ).fetchone()
        assert row is None


@pytest.mark.parametrize(('key', 'data', 'message'), (
    ("mail.ru", {}, b"'key' is a required property"),
    ("mail.ru", {"key": "1"}, b"'value' is a required property"),
    ("mail.ru", {"key": "5", "value": "bla bla", "another": "one"},
     b"Additional properties are not allowed ('another' was unexpected)"),
    ("test", "test", b"payload must be a valid json"),
))
def test_update_validate_input(client, key, data, message):
    with pytest.raises(ValidationError):
        response = client.put(f'/dictionary/{key}',
                              data=json.dumps(data),
                              content_type='application/json')
        assert message in response.data


def test_delete(client, app):
    response = client.delete('/dictionary/test_key')
    assert response.status_code == 200
    assert b"null" in response.data

    with app.app_context():
        row = get_db().execute(
            "select * from dictionary where key = 'test_key'",
        ).fetchone()
        assert row is None


def test_delete_key_not_exist(client):
    response = client.delete('/dictionary/boo')
    assert response.status_code == 200
    assert b"null" in response.data
