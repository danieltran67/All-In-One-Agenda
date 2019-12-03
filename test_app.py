from unittest import TestCase

import flask

import pytest
from flask import request, Flask

import flaskr
from app import db, User, logout
from werkzeug.http import dump_cookie
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


def test_site():
    with app.test_request_context('/?name=Daniel'):
        assert flask.request.path == '/'
        assert flask.request.args['name'] == 'Daniel'


def test_context():
    with app.test_client() as c:
        rv = c.get('/?helloworld=42')
        assert request.args['helloworld'] == '42'


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


class FlaskTestCase(unittest.TestCase):
    # Check that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertFalse(b'Log In' in response.data)

    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post('/login',
                               data=dict(username="admin", password="admin"),
                               follow_redirects=True)
        self.assertTrue(b'You were logged in!', response.data)

    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True)
        self.assertTrue(b'Incorrect username/password. Try again.', response.data)


if __name__ == 'main':
    unittest.main()
