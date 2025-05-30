import pytest   # type: ignore
from unittest.mock import patch
from services.order_service.app import app as order_app

client = order_app.test_client()

@patch('services.order_service.app.requests.get')
def test_create_order_success(mock_get):
    mock_get.return_value.status_code = 200
    data = {'product_id': 1, 'quantity':2}
    resp = client.post('/orders', json=data)
    assert resp.status_code == 201
    assert resp.get_json()['product_id'] == 1

@patch('services.order_service.app.requests.get')
def test_create_order_fail(mock_get):
    mock_get.return_value.status_code = 404
    resp = client.post('/orders', json={'product_id':999})
    assert resp.status_code == 400