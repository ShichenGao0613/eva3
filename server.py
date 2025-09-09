from flask import Flask, request
import json, os
from datetime import datetime

app = Flask(__name__)
os.makedirs("data", exist_ok=True)

@app.route("/submit", methods=["POST"])
def submit():
    payload = request.get_json(force=True)
    payload["_receivedAt"] = datetime.utcnow().isoformat() + "Z"
    with open("data/responses.ndjson", "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)