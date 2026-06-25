import pytest
from app.models import User
from app.extensions import db


@pytest.fixture
def admin_client(client):
    client.post('/auth/register', data={
        'username': 'admin', 'email': 'admin@test.com',
        'password': 'adminpass123', 'confirm': 'adminpass123'
    })
    user = User.query.filter_by(username='admin').first()
    user.is_admin = True
    db.session.commit()
    client.post('/auth/login', data={'username': 'admin', 'password': 'adminpass123'})
    return client


class TestAdminDashboard:
    def test_dashboard_requires_admin(self, client):
        r = client.get('/admin/')
        assert r.status_code in (302, 403)

    def test_dashboard_loads(self, admin_client):
        r = admin_client.get('/admin/')
        assert r.status_code == 200


class TestAdminExport:
    def test_export_all_csv(self, admin_client):
        r = admin_client.get('/admin/export/all')
        assert r.status_code == 200
        assert 'text/csv' in r.content_type

    def test_export_event_csv(self, admin_client, sample_event):
        r = admin_client.get(f'/admin/export/{sample_event.id}')
        assert r.status_code == 200
