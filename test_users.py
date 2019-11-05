import pytest
from app import User


@pytest.fixture(scope='module')
def new_user():
    user = User('testing@gmail.com', 'FlaskIsAwesome')
    return user


def test_new_user(new_user):
    assert test_new_user == 'testing@gmail.com'
    assert new_user.hashed_password != 'FlaskIsAwesome'
    assert not new_user.authenticated
    assert new_user.role == 'user'
