from ai_service import classify_task
import json

result = classify_task("Prepare for coding interview tomorrow")

print("RAW OUTPUT:", result)

try:
    parsed = json.loads(result)
    print("PARSED:", parsed)
except:
    print("❌ JSON parsing failed")