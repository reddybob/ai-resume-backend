from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import os

app = Flask(__name__)

# 🔥 FIX: Strong CORS (frontend connect kosam)
CORS(app, resources={r"/*": {"origins": "*"}})

def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

@app.route("/", methods=["GET"])
def home():
    return "Backend Running 🚀"

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    text = extract_text(file)

    skills = ["python", "java", "sql", "machine learning", "ai"]
    found = [s for s in skills if s in text]

    score = (len(found) / len(skills)) * 100

    return jsonify({
        "score": score,
        "skills": found
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
