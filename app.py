from flask import Flask, request, jsonify
import sqlite3
import os
import keyword

app = Flask(__name__)

DatabasePATH = "data/ravi.db"
os.makedirs(os.path.dirname(DatabasePATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS qna (question TEXT PRIMARY KEY, answer TEXT)")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        description TEXT,
        code_snippet TEXT
    )
""")
conn.commit()


#plan to add one more endpoint to restrict useless codes to be saved for other developers kept like this for now
def is_python_code(snippet):
    python_keywords = keyword.kwlist + ["print", "def", "import"]
    return any(kw in snippet for kw in python_keywords)


#adding snippets
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
        return jsonify({"message": "Snippet added successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Snippet with this title already exists"}), 409

#provide all snippets in the app
@app.route('/list_snippets', methods=['GET'])
def list_snippets():
    cursor.execute("SELECT id, title, description, code_snippet FROM code_snippets")
    data = [{"id": row[0], "title": row[1], "description": row[2], "code_snippet": row[3]} for row in cursor.fetchall()]
    return jsonify({"snippets": data}), 200

#update the code snippets
@app.route('/update_snippet', methods=['PUT'])
def update_snippet():
    data = request.json
    snippet_id = data.get("id")
    title = data.get("title")
    description = data.get("description")
    code_snippet = data.get("code_snippet")
    
    if not snippet_id or not title or not description or not code_snippet:
        return jsonify({"error": "ID, title, description, and code snippet are required"}), 400
    if not is_python_code(code_snippet):
        return jsonify({"error": "Only Python code snippets are allowed"}), 400
    cursor.execute("SELECT * FROM code_snippets WHERE id = ?", (snippet_id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE code_snippets SET title = ?, description = ?, code_snippet = ? WHERE id = ?",
                       (title, description, code_snippet, snippet_id))
        conn.commit()
        return jsonify({"message": "Code snippet updated successfully!"}), 200
    else:
        return jsonify({"error": "Snippet ID not found"}), 404


#deletes the snippet
@app.route('/delete_snippet', methods=['DELETE'])
def delete_snippet():
    snippet_id = request.args.get("id")
    if not snippet_id:
        return jsonify({"error": "ID is required"}), 400
    cursor.execute("SELECT * FROM code_snippets WHERE id = ?", (snippet_id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("DELETE FROM code_snippets WHERE id = ?", (snippet_id,))
        conn.commit()
        return jsonify({"message": "Code snippet deleted successfully!"}), 200
    else:
        return jsonify({"error": "Snippet ID not found"}), 404


if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=10000, debug=True)
