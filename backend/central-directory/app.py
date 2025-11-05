from flask import Flask, jsonify, request


app = Flask(__name__)

# List of branches to sync with
BRANCHES = [
    {"name": "Branch 1", "api": "http://localhost:5001"},
    {"name": "Branch 2", "api": "http://localhost:5002"}
]

# In-memory user store (for now)
USERS = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'server': 'Central Directory'})


# Get all registered branches
@app.route('/branches', methods=['GET'])
def get_branches():
    return jsonify(BRANCHES)


# Add new user (from any branch)
@app.route('/users', methods=['POST'])
def add_user():
    user = request.json
    USERS.append(user)

    # Notify all branches about this new user
    for b in BRANCHES:
        try:
            requests.post(f"{b['api']}/sync/users", json=user, timeout=3)
        except Exception as e:
            print(f"Could not sync with {b['name']}: {e}")

    return jsonify({'message': 'User synced to all branches'}), 201


# Get all users stored in the central directory
@app.route('/users', methods=['GET'])
def list_users():
    return jsonify(USERS)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
