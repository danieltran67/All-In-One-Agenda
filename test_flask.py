import pytest
from project.models import User

@pytest.fixture(scope='module')
def test_index():
  assert title == 'Home'
