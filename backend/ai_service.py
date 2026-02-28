import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def classify_task(task):
    prompt = f"""
You are an AI assistant.

Classify the task into:
- category
- priority (Low, Medium, High)

Return ONLY JSON:
{{
  "category": "",
  "priority": ""
}}

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
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()
    print("DEBUG:", data)
    print("API KEY:", API_KEY)
    return data["choices"][0]["message"]["content"]