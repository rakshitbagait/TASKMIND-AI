from flask import Flask
from flask_cors import CORS
from db import cursor, conn
from flask import request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

from ai_service import classify_task
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running "

def classify_task(task):
    prompt = f"""
    Classify this task into:
    - category
    - priority (Low, Medium, High)

    Return JSON only.

    Task: {task}
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    data = response.json()
    return data["choices"][0]["message"]["content"]
@app.route("/db")
def db():
    cursor.execute("SELECT 1")
    return "database connected"
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    title = data["title"]

    # the ai is called here 
    ai_response = classify_task(title)

    try:
        parsed = json.loads(ai_response)
        category = parsed.get("category", "General")
        priority = parsed.get("priority", "Medium")

    except:
        category = "General"
        priority = "Medium"

    # Store in DB of task mind ai 
    cursor.execute(
        "INSERT INTO tasks (title, category, priority, status) VALUES (%s, %s, %s, %s)",
        (title, category, priority, "Pending")
    )
    conn.commit()

    return jsonify({
        "title": title,
        "category": category,
        "priority": priority
    })
@app.route("/tasks", methods=["GET"])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    result = cursor.fetchall()

    tasks = []
    for row in result:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "category": row[2],
            "priority": row[3],
            "status": row[4]
        })

    return jsonify(tasks)
if __name__ == "__main__":
    app.run(debug=True)