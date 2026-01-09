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
    try:
        data = request.get_json(silent=True) or {}
        print("📝 TEXT INPUT RECEIVED")

        result = run_pipeline(
            input_type="text",
            text=data.get("text", "")
        )

        print("✅ TEXT RESULT GENERATED")

        return jsonify(result or {"summary": "", "flashcards": []})

    except Exception as e:
        print("❌ TEXT API ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ===============================
# PDF INPUT
# ===============================
@app.route("/api/pdf", methods=["POST"])
def pdf_api():
    try:
        file = request.files.get("file")
        print("📄 PDF INPUT RECEIVED")

        if not file:
            return jsonify({"error": "No PDF file uploaded"}), 400

        result = run_pipeline(
            input_type="pdf",
            file=file
        )

        print("✅ PDF RESULT GENERATED")

        return jsonify(result or {"summary": "", "flashcards": []})

    except Exception as e:
        print("❌ PDF API ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ===============================
# IMAGE INPUT
# ===============================
@app.route("/api/image", methods=["POST"])
def image_api():
    try:
        file = request.files.get("file")
        print("🖼 IMAGE INPUT RECEIVED")

        if not file:
            return jsonify({"error": "No image uploaded"}), 400

        result = run_pipeline(
            input_type="image",
            file=file
        )

        print("✅ IMAGE RESULT GENERATED")

        return jsonify(result or {"summary": "", "flashcards": []})

    except Exception as e:
        print("❌ IMAGE API ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ===============================
# VIDEO INPUT
# ===============================
@app.route("/api/video", methods=["POST"])
def video_api():
    try:
        data = request.get_json(silent=True) or {}
        print("🎥 VIDEO INPUT RECEIVED")

        result = run_pipeline(
            input_type="video",
            url=data.get("url", "")
        )

        print("✅ VIDEO RESULT GENERATED")

        return jsonify(result or {"summary": "", "flashcards": []})

    except Exception as e:
        print("❌ VIDEO API ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ===============================
# HEALTH CHECK
# ===============================
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
