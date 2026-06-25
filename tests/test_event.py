from datetime import datetime, timedelta, timezone


EVENT_DATA = {
    'title': 'Test Event',
    'description': 'A test event description',
    'location': 'Campus Hall',
    'start_time': (datetime.now(timezone.utc) + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
    'end_time': (datetime.now(timezone.utc) + timedelta(days=1, hours=2)).strftime('%Y-%m-%dT%H:%M'),
    'max_participants': 50,
    'checkin_code': 'SECRET123',
}


class TestListEvents:
    def test_list_events_empty(self, client):
        resp = client.get('/event/')
        assert resp.status_code == 200


class TestCreateEvent:
    def test_create_event_logged_in(self, auth_client):
        resp = auth_client.post('/event/create', data=EVENT_DATA, follow_redirects=False)
        assert resp.status_code == 302

    def test_create_event_not_logged_in(self, client):
        resp = client.post('/event/create', data=EVENT_DATA, follow_redirects=False)
        assert resp.status_code == 302
        assert 'login' in resp.headers['Location']


class TestEventDetail:
    def test_event_detail(self, client, sample_event):
        resp = client.get(f'/event/{sample_event.id}')
        assert resp.status_code == 200
        assert b'Test Event' in resp.data


class TestEditEvent:
    def test_edit_event(self, auth_client, sample_event):
        resp = auth_client.post(
            f'/event/{sample_event.id}/edit',
            data={**EVENT_DATA, 'title': 'Updated Title'},
            follow_redirects=False,
        )
        assert resp.status_code == 302


class TestDeleteEvent:
    def test_delete_event(self, auth_client, sample_event):
        resp = auth_client.post(
            f'/event/{sample_event.id}/delete',
            follow_redirects=False,
        )
        assert resp.status_code == 302
        assert '/event/' in resp.headers['Location']


class TestEventFull:
    def test_register_when_full(self, app, client):
        from app.models import Event, User
        from app.extensions import db

        client.post('/auth/register', data={
            'username': 'user1', 'email': 'u1@test.com',
            'password': 'pass1234', 'confirm': 'pass1234'
        })
        client.post('/auth/login', data={'username': 'user1', 'password': 'pass1234'})

        now = datetime.now(timezone.utc)
        event = Event(
            title='Full Event',
            description='One spot only',
            location='Room 1',
            start_time=now + timedelta(days=1),
            end_time=now + timedelta(days=1, hours=2),
            max_participants=1,
            checkin_code='CODE1',
            creator_id=1,
        )
        db.session.add(event)
        db.session.commit()

        r1 = client.post(f'/event/{event.id}/register', follow_redirects=False)
        assert r1.status_code == 302

        client.post('/auth/logout')
        client.post('/auth/register', data={
            'username': 'user2', 'email': 'u2@test.com',
            'password': 'pass4567', 'confirm': 'pass4567'
        })
        client.post('/auth/login', data={'username': 'user2', 'password': 'pass4567'})

        r2 = client.post(f'/event/{event.id}/register', follow_redirects=True)
        assert r2.status_code == 200
        assert '名额已满' in r2.data.decode()
