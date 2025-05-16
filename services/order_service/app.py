# services/order-service/app.py
from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

ORDERS = []
PRODUCT_SERVICE_URL = "http://product-service.microservices.svc.cluster.local"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/orders', methods=['GET'])
def list_orders():
    return jsonify(ORDERS)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    # validate product exists
    resp = requests.get(f"{PRODUCT_SERVICE_URL}/products/{data['product_id']}")
    if resp.status_code != 200:
        return jsonify({'error': 'Product not found'}), 400
    order = {
        'id': len(ORDERS) + 1,
        'product_id': data['product_id'],
        'quantity': data.get('quantity', 1)
    }
    ORDERS.append(order)
    return jsonify(order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)