# services/notification-service/app.py
from flask import Flask, request, jsonify  # type: ignore
from flask_sqlalchemy import SQLAlchemy    # type: ignore
import requests
import os

app = Flask(__name__)

# Configure your RDS PostgreSQL connection here
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://microservices_admin_user:terraform-20250528123341691300000007.c5e88my66wu5.us-east-1.rds.amazonaws.com:5432/microservices_platform_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ORDER_SERVICE_URL = os.environ.get("ORDER_SERVICE_URL", "http://order-service.microservices.svc.cluster.local")

# SQLAlchemy model for notifications
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    status = db.Column(db.String(50))

# Auto-create tables if they don't exist
with app.app_context():
    db.create_all()


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/notify', methods=['POST'])
def send_notification():
    data = request.get_json()
    order_id = data.get('order_id')
    # simulate fetching order details
    resp = requests.get(f"{ORDER_SERVICE_URL}/orders")
    if resp.status_code != 200:
        return {'status': 'failed'}, 500
    # Persist notification
    notification = Notification(order_id=order_id, status='sent')
    db.session.add(notification)
    db.session.commit()
    print(f"Notification: Order {order_id} processed.")
    return {'status': 'sent'}


@app.route('/notifications', methods=['GET'])
def list_notifications():
    notifications = Notification.query.all()
    return jsonify([
        {'id': n.id, 'order_id': n.order_id, 'status': n.status}
        for n in notifications
    ])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
