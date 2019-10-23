import os
import tempfile

import pytest

from flask import Flask

@pytest.fixture
def client():
    db_fd, Flask.app.config['DATABASE'] = tempfile.mkstemp()
    Flask.app.config['TESTING'] = True

    with Flask.app.test_client() as client:
        with Flask.app.app_context():
            Flask.init_db()
        yield client

    os.close(db_fd)
    os.unlink(Flask.app.config['DATABASE'])
