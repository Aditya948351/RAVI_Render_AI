from flask import Flask, request, jsonify
import sqlite3
import os
import keyword

app = Flask(__name__)

DB_PATH = "data/ravi.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        description TEXT,
        code_snippet TEXT
    )
""")
conn.commit()

def is_python_code(snippet):
    return any(kw in snippet for kw in keyword.kwlist + ["print", "def", "import"])

@app.route('/add_snippet', methods=['POST'])
def add_snippet():
    data = request.json
    title, description, code_snippet = data.get("title"), data.get("description"), data.get("code_snippet")
    
    if not all([title, description, code_snippet]):
        return jsonify({"error": "All fields are required"}), 400
    
    if not is_python_code(code_snippet):
        return jsonify({"error": "Only Python code snippets are allowed"}), 400
    
    try:
        cursor.execute("INSERT INTO code_snippets (title, description, code_snippet) VALUES (?, ?, ?)",
                       (title, description, code_snippet))
        conn.commit()
        return jsonify({"message": "Snippet added successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Snippet with this title already exists"}), 409

@app.route('/list_snippets', methods=['GET'])
def list_snippets():
    cursor.execute("SELECT id, title, description, code_snippet FROM code_snippets")
    return jsonify({"snippets": [dict(zip(["id", "title", "description", "code_snippet"], row)) for row in cursor.fetchall()]}), 200

@app.route('/update_snippet', methods=['PUT'])
def update_snippet():
    data = request.json
    snippet_id, title, description, code_snippet = data.get("id"), data.get("title"), data.get("description"), data.get("code_snippet")
    
    if not all([snippet_id, title, description, code_snippet]):
        return jsonify({"error": "All fields are required"}), 400
    
    if not is_python_code(code_snippet):
        return jsonify({"error": "Only Python code snippets are allowed"}), 400
    
    cursor.execute("SELECT * FROM code_snippets WHERE id = ?", (snippet_id,))
    if cursor.fetchone():
        cursor.execute("UPDATE code_snippets SET title = ?, description = ?, code_snippet = ? WHERE id = ?",
                       (title, description, code_snippet, snippet_id))
        conn.commit()
        return jsonify({"message": "Snippet updated successfully!"}), 200
    return jsonify({"error": "Snippet ID not found"}), 404

@app.route('/delete_snippet', methods=['DELETE'])
def delete_snippet():
    snippet_id = request.args.get("id")
    
    if not snippet_id:
        return jsonify({"error": "ID is required"}), 400
    
    cursor.execute("SELECT * FROM code_snippets WHERE id = ?", (snippet_id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM code_snippets WHERE id = ?", (snippet_id,))
        conn.commit()
        return jsonify({"message": "Code snippet deleted successfully!"}), 200
    return jsonify({"error": "Snippet ID not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
