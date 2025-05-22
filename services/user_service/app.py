from flask import Flask, jsonify, request, abort  # type: ignore
app = Flask(__name__)

# In-memory store
users = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'}
]


# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/users', methods=['GET'])
def list_users():
    return jsonify(users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    u = next((u for u in users if u['id'] == user_id), None)
    if not u:
        abort(404)
    return jsonify(u)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400)
    new_id = max(u['id'] for u in users) + 1
    user = {'id': new_id, 'name': data['name']}
    users.append(user)
    return jsonify(user), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    u = next((u for u in users if u['id'] == user_id), None)
    if not u:
        abort(404)
    if not data or 'name' not in data:
        abort(400)
    u['name'] = data['name']  # type: ignore
    return jsonify(u)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
