from sniffr.app import create_app
import pytest
from sniffr.models import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def new_user():
    user = User('danny@d300.org', 'gancho')
    return user