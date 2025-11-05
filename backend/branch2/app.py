from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'branch': 'B'})

@app.route('/books', methods=['GET'])
def get_books():
    # TODO: connect to MySQL and return books for Branch B
    return jsonify([])

# Sync route — receives user data from central directory
@app.route('/sync/users', methods=['POST'])
def sync_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
    existing = cursor.fetchone()

    if not existing:
        cursor.execute("""
            INSERT INTO users (name, email, registered_branch)
            VALUES (%s, %s, %s)
        """, (data['name'], data['email'], data['registered_branch']))
        conn.commit()

    cursor.close()
    conn.close()
    return jsonify({'message': 'User synced successfully'}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)
