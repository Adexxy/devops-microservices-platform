# services/product-service/app.py
from flask import Flask, jsonify, request  # type: ignore
app = Flask(__name__)

# In-memory product store
products = [
    {'id': 1, 'name': 'Widget', 'price': 9.99},
    {'id': 2, 'name': 'Gadget', 'price': 12.49}
]


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(products)


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    p = next((p for p in products if p['id'] == product_id), None)
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(p)


@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_id = max(p['id'] for p in products) + 1
    product = {'id': new_id, 'name': data['name'], 'price': data['price']}
    products.append(product)
    return jsonify(product), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
