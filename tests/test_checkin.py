class TestCheckin:
    def test_register_for_event(self, auth_client, sample_event):
        resp = auth_client.post(
            f'/event/{sample_event.id}/register',
            follow_redirects=False,
        )
        assert resp.status_code == 302

    def test_checkin_correct_code(self, auth_client, sample_event):
        auth_client.post(f'/event/{sample_event.id}/register')
        resp = auth_client.post(
            f'/checkin/{sample_event.id}',
            data={'code': 'ABC123'},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert '签到成功' in resp.data.decode()

    def test_checkin_wrong_code(self, auth_client, sample_event):
        auth_client.post(f'/event/{sample_event.id}/register')
        resp = auth_client.post(
            f'/checkin/{sample_event.id}',
            data={'code': 'WRONG'},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert '签到码错误' in resp.data.decode()

    def test_checkin_without_registration(self, auth_client, sample_event):
        resp = auth_client.post(
            f'/checkin/{sample_event.id}',
            data={'code': 'ABC123'},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert '尚未报名' in resp.data.decode()

    def test_checkin_twice(self, auth_client, sample_event):
        auth_client.post(f'/event/{sample_event.id}/register')
        auth_client.post(f'/checkin/{sample_event.id}', data={'code': 'ABC123'})
        resp = auth_client.post(
            f'/checkin/{sample_event.id}',
            data={'code': 'ABC123'},
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert '已经签到过了' in resp.data.decode()
