from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection details from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "your_db")
DB_USER = os.getenv("DB_USER", "your_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")

# Establish connection to PostgreSQL database
def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        name = data['name']
        email = data['email']

        # Insert data into the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Data submitted successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error processing request"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
