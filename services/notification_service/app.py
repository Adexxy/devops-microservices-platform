# services/notification-service/app.py
from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

ORDER_SERVICE_URL = "http://order-service.microservices.svc.cluster.local"

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
    # In real-world, push to email/SMS queue
    print(f"Notification: Order {{order_id}} processed.")
    return {'status': 'sent'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
