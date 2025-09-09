from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, re
from datetime import datetime

app = Flask(__name__)

CORS(
    app,
    resources={r"/submit": {"origins": "*"}},
    supports_credentials=False,
    allow_headers=["Content-Type", "ngrok-skip-browser-warning"],
    methods=["POST", "OPTIONS"],
    max_age=86400,
)

BASE_DIR = "submissions"
os.makedirs(BASE_DIR, exist_ok=True)

SAFE = re.compile(r"[^A-Za-z0-9._-]") 
def sanitize(s, default="unknown"):
    if not s:
        return default
    out = SAFE.sub("_", str(s))
    return out[:80]  

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"ok": False, "error": "invalid JSON"}), 400

    prolific = data.get("prolific") or {}
    pid = sanitize(prolific.get("pid"), "anonymous")  
    sid = sanitize(prolific.get("sessionId") or data.get("submissionId") or datetime.utcnow().strftime("noid-%Y%m%dT%H%M%S"))


    part_dir = os.path.join(BASE_DIR, pid)
    os.makedirs(part_dir, exist_ok=True)

    path = os.path.join(part_dir, f"{sid}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return jsonify({"ok": True, "saved": path})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)