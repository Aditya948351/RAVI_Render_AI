from flask import Flask, request, jsonify
import sqlite3
import os
import re

app = Flask(__name__)

# Ensure data directory exists
DB_PATH = "data/ravi.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# Create QnA Table
cursor.execute("CREATE TABLE IF NOT EXISTS qna (question TEXT PRIMARY KEY, answer TEXT)")

# Create Code Snippets Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        description TEXT,
        code_snippet TEXT
    )
""")
conn.commit()


# Function to check if the snippet is Python code
def is_python_code(snippet):
    return bool(re.match(r"^\s*(import |from |def |class )", snippet, re.MULTILINE))


@app.route('/add_snippet', methods=['POST'])
def add_snippet():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    code_snippet = data.get("code_snippet")

    if not title or not description or not code_snippet:
        return jsonify({"error": "Title, description, and code snippet are required"}), 400

    if not is_python_code(code_snippet):
        return jsonify({"error": "Only Python code snippets are allowed"}), 400

    try:
        cursor.execute("INSERT INTO code_snippets (title, description, code_snippet) VALUES (?, ?, ?)",
                       (title, description, code_snippet))
        conn.commit()
        return jsonify({"message": "Code snippet added successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Title already exists"}), 409


@app.route('/list_snippets', methods=['GET'])
def list_snippets():
    cursor.execute("SELECT title, description, code_snippet FROM code_snippets")
    data = [{"title": row[0], "description": row[1], "code_snippet": row[2]} for row in cursor.fetchall()]
    return jsonify({"snippets": data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
