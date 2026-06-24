class TestRegister:
    def test_register_success(self, client):
        resp = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'testpass123',
            'confirm': 'testpass123',
        }, follow_redirects=False)
        assert resp.status_code == 302
        assert '/auth/login' in resp.headers['Location']

    def test_register_duplicate_username(self, client):
        client.post('/auth/register', data={
            'username': 'dupuser',
            'email': 'dup@test.com',
            'password': 'testpass123',
            'confirm': 'testpass123',
        })
        resp = client.post('/auth/register', data={
            'username': 'dupuser',
            'email': 'other@test.com',
            'password': 'testpass123',
            'confirm': 'testpass123',
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert '用户名已存在' in resp.data.decode()


class TestLogin:
    def test_login_success(self, client):
        client.post('/auth/register', data={
            'username': 'loginuser',
            'email': 'login@test.com',
            'password': 'testpass123',
            'confirm': 'testpass123',
        })
        resp = client.post('/auth/login', data={
            'username': 'loginuser',
            'password': 'testpass123',
        }, follow_redirects=False)
        assert resp.status_code == 302

    def test_login_wrong_password(self, client):
        client.post('/auth/register', data={
            'username': 'loginuser2',
            'email': 'login2@test.com',
            'password': 'testpass123',
            'confirm': 'testpass123',
        })
        resp = client.post('/auth/login', data={
            'username': 'loginuser2',
            'password': 'wrongpassword',
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert '用户名或密码错误' in resp.data.decode()


class TestLogout:
    def test_logout(self, auth_client):
        resp = auth_client.post('/auth/logout', follow_redirects=False)
        assert resp.status_code == 302
        assert '/auth/login' in resp.headers['Location']
