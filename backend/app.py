from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from urllib.parse import urlparse
from textblob import TextBlob
import nltk
import os

# Ensure NLTK resources are available
nltk.download("punkt")

# Initialize Flask app
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "backend", "templates"))
CORS(app)

# Trusted News Sources
TRUSTED_SOURCES = {
    "bbc.com": "High",
    "reuters.com": "High",
    "nytimes.com": "Medium",
    "foxnews.com": "Medium",
    "indianexpress.com": "Medium"
}

def detect_bias(text):
    """Detects bias based on subjectivity and highlights biased words."""
    blob = TextBlob(text)
    subjectivity = blob.sentiment.subjectivity  # 0 = factual, 1 = highly biased
    bias_score = round(subjectivity * 100, 2)

    words = text.split()
    biased_words = [word for word in words if TextBlob(word).sentiment.subjectivity > 0.3]  # Lowered threshold

    return "Bias Detected" if bias_score > 20 else "No bias detected", bias_score, biased_words

def highlight_bias(original):
    """Highlights biased words in red without rewriting text."""
    words = original.split()
    highlighted_text = []

    for word in words:
        if TextBlob(word).sentiment.subjectivity > 0.3:  # Biased word threshold
            highlighted_text.append(f"<span style='color: red; text-decoration: underline;'>{word}</span>")
        else:
            highlighted_text.append(word)

    return " ".join(highlighted_text)

def get_source_rating(url):
    """Checks credibility of a news source."""
    domain = urlparse(url).netloc.replace("www.", "")

    for source in TRUSTED_SOURCES:
        if source in domain:
            return TRUSTED_SOURCES[source]

    return "No Verified Data Available"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyzes text for bias and highlights biased words."""
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Invalid JSON input"}), 400

        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "No text provided"}), 400

        bias_category, bias_score, biased_words = detect_bias(text)
        highlighted_text = highlight_bias(text)

        response = {
            "original": text,
            "redlined_text": highlighted_text,
            "biased_words": biased_words,
            "bias_category": bias_category,
            "bias_score": bias_score
        }

        return jsonify(response)

    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({"error": "Server Error", "details": str(e)}), 500

@app.route('/source_check', methods=['POST'])
def source_check():
    """Checks credibility of a news source."""
    data = request.get_json()
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    return jsonify({"source_rating": get_source_rating(url)})

@app.route('/flag', methods=['POST'])
def flag_article():
    """Flags an article for review."""
    try:
        data = request.get_json()
        flagged_text = data.get("flagged_text", "").strip()
        if not flagged_text:
            return jsonify({"error": "No article text provided"}), 400

        print(f"⚠️ Article Flagged for Review: {flagged_text[:100]}...")
        return jsonify({"message": "Article flagged successfully!"})

    except Exception as e:
        print(f"❌ Flagging Error: {e}")
        return jsonify({"error": "Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)










































