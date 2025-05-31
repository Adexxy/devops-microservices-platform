# services/order-service/app.py
from flask import Flask, jsonify, request  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import requests
import os

app = Flask(__name__)

# ORDERS = []
# Configure your RDS PostgreSQL connection here
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://microservices_admin_user:terraform-20250528123341691300000007.c5e88my66wu5.us-east-1.rds.amazonaws.com:5432/microservices_platform_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# PRODUCT_SERVICE_URL = "http://product-service.microservices.svc.cluster.local"
# In order_service/app.py
PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL", "http://product_service:5002")

# SQLAlchemy model for orders
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

# Auto-create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/orders', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    return jsonify([
        {'id': o.id, 'product_id': o.product_id, 'quantity': o.quantity}
        for o in orders
    ])


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    # validate product exists
    resp = requests.get(f"{PRODUCT_SERVICE_URL}/products/{data['product_id']}")
    if resp.status_code != 200:
        return jsonify({'error': 'Product not found'}), 400
    order = Order(product_id=data['product_id'], quantity=data.get('quantity', 1))
    db.session.add(order)
    db.session.commit()
    return jsonify({'id': order.id, 'product_id': order.product_id, 'quantity': order.quantity}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
