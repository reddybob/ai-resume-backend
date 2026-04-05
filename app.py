from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # 🔥 Important (frontend connect avvadanki)

# Job descriptions (AI comparison kosam)
job_descriptions = {
    "python": "python django flask sql backend developer programming api development software engineer",
    "data": "machine learning python pandas numpy data analysis statistics deep learning ai",
    "web": "html css javascript react frontend developer web design ui ux",
    "ai": "artificial intelligence deep learning neural networks python tensorflow keras",
    "ml": "machine learning python scikit-learn pandas numpy data science models",
    "cloud": "aws azure cloud computing devops docker kubernetes linux",
    "cyber": "cyber security networking ethical hacking penetration testing kali linux"
}

# Resume nundi text extract
def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# AI matching (TF-IDF + Cosine Similarity)
def match_resume(resume_text, job_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_text])
    
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = similarity * 100 * 5
    return round(min(score, 100), 2)

# API route
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    job = request.form['job']

    resume_text = extract_text(file)
    job_text = job_descriptions[job]

    match = match_resume(resume_text, job_text)

    return jsonify({
        "match": match
    })

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)