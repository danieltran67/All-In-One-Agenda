
import flask

import pytest
from flask import request
from app import db, User
import unittest

app = flask.Flask(__name__)


@pytest.mark.django_db
def test_my_user():
    me = User(username='me')
    assert me


def test_database():
    user = User()
    db.session.add(user)
    db.session.commit()

    assert user in db.session


class SomeTest:
    pass


def test_site():
    with app.test_request_context('/?name=Peter'):
        assert flask.request.path == '/'
        assert flask.request.args['name'] == 'Peter'


def test_context():
    with app.test_client() as c:
        rv = c.get('/?tequila=42')
        assert request.args['tequila'] == '42'


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


if __name__ == 'main':
    unittest.main()
