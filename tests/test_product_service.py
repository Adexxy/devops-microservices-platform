import pytest   # type: ignore
from services.product_service.app import app as product_app

test_client = product_app.test_client()

@pytest.fixture
def client():
    return product_app.test_client()

def test_health():
    resp = test_client.get('/health')
    assert resp.status_code == 200

# def test_list_and_get():
#     resp = test_client.get('/products')
#     assert resp.status_code == 200
#     products = resp.get_json()
#     assert isinstance(products, list)
#     pid = products[0]['id']
#     resp2 = test_client.get(f'/products/{pid}')
#     assert resp2.status_code == 200


def test_list_and_get(client):
    # Create a product first
    resp = client.post('/products', json={'name': 'Test', 'price': 10.0})
    assert resp.status_code == 201
    product_id = resp.get_json()['id']

    # Now list products
    resp = client.get('/products')
    products = resp.get_json()
    assert len(products) > 0

    # Get the product by ID
    resp = client.get(f'/products/{product_id}')
    assert resp.status_code == 200


def test_create_product():
    resp = test_client.post('/products', json={'name':'Thing','price':5.0})
    assert resp.status_code == 201
    assert 'id' in resp.get_json()