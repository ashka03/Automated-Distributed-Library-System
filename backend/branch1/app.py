from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# --- MySQL Database Configuration ---
db_config = {
    'host': 'localhost',
    'user': 'root',             # or your MySQL username
    'password': 'Bhavjay2394!',# replace with your password
    'database': 'library_branch1'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn


# --- ROUTES ---
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'branch': 'A'})


# Fetch all books
@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, genre, available, branch_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (data['title'], data['author'], data['genre'], data.get('available', True), data['branch_id']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Book added successfully'}), 201


# Borrow a book (loan)
@app.route('/loans', methods=['POST'])
def borrow_book():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check availability
    cursor.execute("SELECT available FROM books WHERE book_id = %s", (data['book_id'],))
    available = cursor.fetchone()
    if not available or not available[0]:
        return jsonify({'error': 'Book not available'}), 400

    # Create loan record
    cursor.execute("""
        INSERT INTO loans (book_id, user_id, issue_date, due_date, branch_id)
        VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), %s)
    """, (data['book_id'], data['user_id'], data['branch_id']))

    # Update availability
    cursor.execute("UPDATE books SET available = FALSE WHERE book_id = %s", (data['book_id'],))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({'message': 'Book borrowed successfully'}), 201


# Return a book
@app.route('/loans/<int:loan_id>/return', methods=['PUT'])
def return_book(loan_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update loan and book availability
    cursor.execute("""
        UPDATE loans SET return_date = CURDATE(), status = 'returned'
        WHERE loan_id = %s
    """, (loan_id,))
    cursor.execute("""
        UPDATE books 
        SET available = TRUE 
        WHERE book_id = (SELECT book_id FROM loans WHERE loan_id = %s)
    """, (loan_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({'message': 'Book returned successfully'})

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
    app.run(host='0.0.0.0', port=5001, debug=True)
