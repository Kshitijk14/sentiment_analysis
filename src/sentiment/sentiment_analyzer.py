from transformers import pipeline

# Load model once
sentiment_pipeline = pipeline("sentiment-analysis", model="tabularisai/multilingual-sentiment-analysis")

def analyze_sentiment(texts):
    """Run sentiment analysis on list of texts"""
    return sentiment_pipeline(texts)
