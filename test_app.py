"""
  import pytest
from models import User


@pytest.fixture(scope='module')
def new_user():
    user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    return user


def test_new_user(new_user):
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.hashed_password != 'FlaskIsAwesome'
    assert not new_user.authenticated
    assert new_user.role == 'user'
  """
import flask
import os

from django.core import mail
from flask import Flask, request
from app import db, User
import unittest
from flask_testing import LiveServerTestCase

app = flask.Flask(__name__)


def test_database():
    user = User()
    db.session.add(user)
    db.session.commit()

    assert user in db.session


def test_name():
    name = User(username='Daniel')

    db.session.add(name)
    db.session.commit()

    assert name in db.session


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
