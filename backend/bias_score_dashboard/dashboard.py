import sys
import nltk
from difflib import ndiff
from transformers import pipeline

sys.stdout.reconfigure(encoding='utf-8')


nltk.download('punkt')

bias_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def detect_bias_advanced(text):
    """Use AI to detect bias dynamically."""
    try:
        categories = ["Neutral", "Left Bias", "Right Bias", "Sensational", "Opinion"]
        result = bias_classifier(text, candidate_labels=categories)

        print(f"🎯 AI Bias Detection Results: {result}")  
        return result
    except Exception as e:
        print(f"❌ Error in AI Bias Detection: {str(e)}")
        return {"labels": ["Neutral"], "scores": [1.0]}  


def rewrite_article(text):
    """Use AI to rewrite the article in a neutral way."""
    try:
        rewritten = summarizer(text, max_length=300, min_length=100, do_sample=False)
        return rewritten[0]['summary_text']
    except Exception as e:
        print(f"❌ Error in AI Rewriting: {str(e)}")
        return text 

def predict_bias_score(text):
    """Use AI to determine bias score based on detected bias categories."""
    try:
        result = detect_bias_advanced(text)

        
        bias_score = sum([score * 100 for label, score in zip(result["labels"], result["scores"]) if label != "Neutral"])

        return round(bias_score, 2)  
    except Exception as e:
        print(f"❌ Error in Bias Score Calculation: {str(e)}")
        return 0.0  # Default to 0 if AI fails


def highlight_changes(original, rewritten):
    """Compare original and rewritten text to detect changes."""
    try:
        changes = list(ndiff(original.split(), rewritten.split()))
        explained_changes = [
            f"✅ Changed: {change[2:]}" if change.startswith("+ ") else f"❌ Removed: {change[2:]}"
            for change in changes if change.startswith("+ ") or change.startswith("- ")
        ]
        return explained_changes if explained_changes else ["No significant changes."]
    except Exception as e:
        print(f"❌ Error in Highlighting Changes: {str(e)}")
        return ["Error detecting changes."]



