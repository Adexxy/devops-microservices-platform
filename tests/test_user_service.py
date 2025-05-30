import pytest   # type: ignore
from services.user_service.app import app as user_app

test_client = user_app.test_client()

def test_health():
    resp = test_client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json() == {'status': 'ok'}

def test_create_and_get_user():
    # Create
    resp = test_client.post('/users', json={'name': 'Charlie'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'id' in data and data['name'] == 'Charlie'
    uid = data['id']
    # Retrieve
    resp2 = test_client.get(f'/users/{uid}')
    assert resp2.status_code == 200
    assert resp2.get_json()['name'] == 'Charlie'

def test_update_user():
    # Create dummy
    resp = test_client.post('/users', json={'name': 'Dave'})
    uid = resp.get_json()['id']
    # Update
    resp2 = test_client.put(f'/users/{uid}', json={'name': 'David'})
    assert resp2.status_code == 200
    assert resp2.get_json()['name'] == 'David'

def test_delete_user():
    resp = test_client.post('/users', json={'name': 'Eve'})
    uid = resp.get_json()['id']
    resp2 = test_client.delete(f'/users/{uid}')
    assert resp2.status_code == 204
    # Verify gone
    resp3 = test_client.get(f'/users/{uid}')
    assert resp3.status_code == 404