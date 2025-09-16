from transformers import pipeline

from utils.config import CONFIG


SENTIMENT_ANALYSIS_TASK = CONFIG["SENTIMENT_ANALYSIS_TASK"]
SENTIMENT_ANALYSIS_MODEL = CONFIG["SENTIMENT_ANALYSIS_MODEL"]


# Load model once
sentiment_pipeline = pipeline(SENTIMENT_ANALYSIS_TASK, model=SENTIMENT_ANALYSIS_MODEL)


def analyze_sentiment(texts):
    """Run sentiment analysis on list of texts"""
    return sentiment_pipeline(texts)
