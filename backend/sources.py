# backend/sources.py
from urllib.parse import urlparse

TRUSTED_SOURCES = {
    "bbc.com": "High",
    "nytimes.com": "High",
    "foxnews.com": "Medium",
    "infowars.com": "Low",
    "indianexpress.com": "High",
    "reuters.com": "High",
    "theguardian.com": "High",
    "breitbart.com": "Low",
    "oann.com": "Low"
}

def extract_domain(url):
    """Extracts domain name from URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")
    return domain

def verify_sources(article_text):
    """Find relevant sources in the article text."""
    found_sources = [source for source in TRUSTED_SOURCES if source in article_text]
    return found_sources if found_sources else ["No recognized sources found"]

def get_source_rating(url):
    """Returns credibility rating of a news source URL."""
    domain = extract_domain(url)
    return TRUSTED_SOURCES.get(domain, "Unknown")

