from sniffr.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User('danny@d300.org', 'gancho')
    assert user.email == 'danny@d300.org'
