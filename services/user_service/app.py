from flask import Flask, jsonify, request, abort  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import os

app = Flask(__name__)

# Configure your RDS PostgreSQL connection here
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://microservices_admin_user:terraform-20250528123341691300000007.c5e88my66wu5.us-east-1.rds.amazonaws.com:5432/microservices_platform_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SQLAlchemy model for users
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

# Auto-create tables if they don't exist
with app.app_context():
    db.create_all()


# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name} for u in users])


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    u = User.query.get(user_id)
    if not u:
        abort(404)
    return jsonify({'id': u.id, 'name': u.name})


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400)
    user = User(name=data['name'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name}), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    if not data or 'name' not in data:
        abort(400)
    user.name = data['name']
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name})


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
