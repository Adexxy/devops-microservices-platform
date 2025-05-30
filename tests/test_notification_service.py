import pytest   # type: ignore
from unittest.mock import patch
from services.notification_service.app import app as notif_app


client = notif_app.test_client()

def test_health():
    resp = client.get('/health')
    assert resp.status_code == 200

@patch('services.notification_service.app.requests.get')
def test_notify(mock_get):
    mock_get.return_value.status_code = 200
    resp = client.post('/notify', json={'order_id':1})
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'sent'