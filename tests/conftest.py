import pytest
from app import create_app
from app.extensions import db
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    client.post('/auth/register', data={
        'username': 'testuser', 'email': 'test@test.com',
        'password': 'testpass123', 'confirm': 'testpass123'
    })
    client.post('/auth/login', data={'username': 'testuser', 'password': 'testpass123'})
    return client


@pytest.fixture
def sample_event(app, auth_client):
    from datetime import datetime, timedelta, timezone
    from app.models import Event
    from app.extensions import db

    now = datetime.now(timezone.utc)
    event = Event(
        title='Test Event',
        description='A test event',
        location='Test Location',
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=2),
        max_participants=50,
        checkin_code='ABC123',
        creator_id=1,
    )
    db.session.add(event)
    db.session.commit()
    return event
