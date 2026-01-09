from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from core.orchestrator import run_pipeline

load_dotenv()

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

CORS(app)


# ===============================
# FRONTEND PAGE
# ===============================
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# ===============================
# TEXT INPUT
# ===============================
@app.route("/api/text", methods=["POST"])
def text_api():
    data = request.get_json(silent=True) or {}
    result = run_pipeline(
        input_type="text",
        text=data.get("text", "")
    )
    return jsonify(result)


# ===============================
# PDF INPUT
# ===============================
@app.route("/api/pdf", methods=["POST"])
def pdf_api():
    file = request.files.get("file")
    result = run_pipeline(
        input_type="pdf",
        file=file
    )
    return jsonify(result)


# ===============================
# IMAGE INPUT
# ===============================
@app.route("/api/image", methods=["POST"])
def image_api():
    file = request.files.get("file")
    result = run_pipeline(
        input_type="image",
        file=file
    )
    return jsonify(result)


# ===============================
# VIDEO INPUT
# ===============================
@app.route("/api/video", methods=["POST"])
def video_api():
    data = request.get_json(silent=True) or {}
    result = run_pipeline(
        input_type="video",
        url=data.get("url", "")
    )
    return jsonify(result)


# ===============================
# HEALTH CHECK
# ===============================
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
