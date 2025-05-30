# services/product-service/app.py
from flask import Flask, jsonify, request  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import os

app = Flask(__name__)

# Configure your RDS PostgreSQL connection here
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://microservices_admin_user:terraform-20250528123341691300000007.c5e88my66wu5.us-east-1.rds.amazonaws.com:5432/microservices_platform_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SQLAlchemy model for products
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))

# Auto-create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([
        {'id': p.id, 'name': p.name, 'price': float(p.price)}
        for p in products
    ])


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    p = Product.query.get(product_id)
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'id': p.id, 'name': p.name, 'price': float(p.price)})


@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id, 'name': product.name, 'price': float(product.price)}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
