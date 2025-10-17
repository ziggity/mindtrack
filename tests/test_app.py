import pytest
from app import app, db, User

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        with app.test_client() as testing_client:
            yield testing_client
        db.drop_all()

def test_signup_with_whitespace_password_fails(test_client):
    """
    GIVEN a Flask application
    WHEN a user tries to sign up with a password containing only whitespace
    THEN the signup should fail and the user should not be created
    """
    response = test_client.post('/signup', data={
        'username': 'testuser',
        'password': '   '
    }, follow_redirects=True)

    assert response.status_code == 200
    user = User.query.filter_by(username='testuser').first()
    assert user is None