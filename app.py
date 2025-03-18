from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Ensure data directory exists
DB_PATH = "data/ravi.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS qna (question TEXT PRIMARY KEY, answer TEXT)")
conn.commit()


@app.route('/add_qna', methods=['POST'])
def add_qna():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return jsonify({"error": "Both question and answer are required"}), 400

    try:
        cursor.execute("INSERT INTO qna (question, answer) VALUES (?, ?)", (question.lower(), answer))
        conn.commit()
        return jsonify({"message": "QnA added successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Question already exists"}), 409


@app.route('/update_qna', methods=['PUT'])
def update_qna():
    data = request.json
    question = data.get("question")
    new_answer = data.get("new_answer")

    if not question or not new_answer:
        return jsonify({"error": "Both question and new answer are required"}), 400

    cursor.execute("SELECT answer FROM qna WHERE question = ?", (question.lower(),))
    result = cursor.fetchone()

    if result:
        cursor.execute("UPDATE qna SET answer = ? WHERE question = ?", (new_answer, question.lower()))
        conn.commit()
        return jsonify({"message": "QnA updated successfully!"}), 200
    else:
        return jsonify({"error": "Question not found"}), 404


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question").strip().lower()

    if not question:
        return jsonify({"error": "Question is required"}), 400

    cursor.execute("SELECT answer FROM qna WHERE question = ?", (question,))
    result = cursor.fetchone()

    if result:
        return jsonify({"answer": result[0]})

    return jsonify({"answer": "I don't know. Please add this answer manually."})


@app.route('/list_qna', methods=['GET'])
def list_qna():
    cursor.execute("SELECT question, answer FROM qna")
    data = [{"question": row[0], "answer": row[1]} for row in cursor.fetchall()]
    return jsonify({"qna_list": data})


@app.route('/delete_qna', methods=['DELETE'])
def delete_qna():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    cursor.execute("DELETE FROM qna WHERE question = ?", (question.lower(),))
    conn.commit()
    return jsonify({"message": "QnA deleted successfully!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

