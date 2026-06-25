def test_translate_zh_to_en(client):
    r = client.post('/api/translate', json={'text': '学术', 'target': 'en'})
    assert r.status_code == 200
    assert r.get_json()['translated'] == 'Academic'


def test_translate_missing_text(client):
    r = client.post('/api/translate', json={})
    assert r.status_code == 400


def test_events_bilingual(client):
    r = client.get('/api/events')
    assert r.status_code == 200
