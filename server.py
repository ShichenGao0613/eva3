from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json
from datetime import datetime

app = Flask(__name__)

CORS(app, resources={r"/submit": {"origins": "*"}}, supports_credentials=False)

os.makedirs("submissions", exist_ok=True)

@app.route("/submit", methods=["POST", "OPTIONS"])
def submit():
    
    if request.method == "OPTIONS":
        resp = app.make_response(("", 204))
        resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
       
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, ngrok-skip-browser-warning"
        return resp

    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"ok": False, "error": "invalid JSON"}), 400

    sub_id = data.get("submissionId") or datetime.utcnow().strftime("noid-%Y%m%dT%H%M%S")
    path = os.path.join("submissions", f"{sub_id}.json")


    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return jsonify({"ok": True, "saved": path})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)