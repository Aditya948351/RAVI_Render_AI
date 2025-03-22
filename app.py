from flask import Flask, request, jsonify
 import sqlite3
 import os
 import re
 import keyword
 
 app = Flask(__name__)
 
 @@ -27,35 +27,41 @@
 """)
 conn.commit()
 
 # Function to validate Python code snippets
 def is_python_code(snippet):
     python_keywords = keyword.kwlist + ["print", "def", "import"]
     return any(kw in snippet for kw in python_keywords)
 
 
 # Add a new code snippet
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
 
     cursor.execute("INSERT INTO snippets (title, description, code_snippet) VALUES (?, ?, ?)",
                    (title, description, code_snippet))
     conn.commit()
 
     return jsonify({"message": "Snippet added successfully!"}), 201
 
     try:
         cursor.execute("INSERT INTO code_snippets (title, description, code_snippet) VALUES (?, ?, ?)",
                        (title, description, code_snippet))
         conn.commit()
         return jsonify({"message": "Snippet added successfully!"}), 201
     except sqlite3.IntegrityError:
         return jsonify({"error": "Snippet with this title already exists"}), 409
 
 # List all snippets
 @app.route('/list_snippets', methods=['GET'])
 def list_snippets():
     cursor.execute("SELECT id, title, description, code_snippet FROM code_snippets")
     data = [{"id": row[0], "title": row[1], "description": row[2], "code_snippet": row[3]} for row in cursor.fetchall()]
     return jsonify({"snippets": data})
 
     return jsonify({"snippets": data}), 200
 
 # Update an existing snippet
 @app.route('/update_snippet', methods=['PUT'])
 def update_snippet():
     data = request.json
 @@ -80,12 +86,9 @@ def update_snippet():
         return jsonify({"message": "Code snippet updated successfully!"}), 200
     else:
         return jsonify({"error": "Snippet ID not found"}), 404
 
 
 @app.route('/delete_snippet', methods=['DELETE'])
 def delete_snippet():
     data = request.json
     snippet_id = data.get("id")
     snippet_id = request.args.get("id")  # Use request.args for DELETE
 
     if not snippet_id:
         return jsonify({"error": "ID is required"}), 400
 @@ -99,7 +102,5 @@ def delete_snippet():
         return jsonify({"message": "Code snippet deleted successfully!"}), 200
     else:
         return jsonify({"error": "Snippet ID not found"}), 404
 
 
 if __name__ == '__main__':
     app.run(host='0.0.0.0', port=10000, debug=True)
