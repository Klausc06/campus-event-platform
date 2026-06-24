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
