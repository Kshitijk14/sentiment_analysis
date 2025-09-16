import os

from utils.collectors.twitter_collector import fetch_tweets
from utils.preprocessing.text_cleaner import clean_text
from utils.models.sentiment_analyzer import analyze_sentiment
from utils.helpers.email_alerts import send_email_alert

from utils.config import CONFIG
from utils.logger import setup_logger


# configs
LOG_PATH = CONFIG["LOG_PATH"]
MAX_RESULTS = CONFIG["MAX_RESULTS"]
PIPELINE_SENTIMENT_THRESHOLD = CONFIG["PIPELINE_SENTIMENT_THRESHOLD"]

# setup logger
LOG_DIR = os.path.join(os.getcwd(), LOG_PATH)
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "main.log")


def run_pipeline(logger):    
    logger.info("[Step 1]: Collect data from Twitter")
    tweets = fetch_tweets("Samsung", MAX_RESULTS, logger)
    if not tweets:
        logger.warning("No tweets found for this query.")
        return

    logger.info("[Step 2]: Preprocess")
    for t in tweets:
        t["cleaned_text"] = clean_text(t["text"], logger)
        logger.debug(f"Original: {t['text']}\nCleaned: {t['cleaned_text']}\n")

    logger.info("[Step 3]: Sentiment Analysis")
    texts = [t["cleaned_text"] for t in tweets if t["cleaned_text"]]
    results = analyze_sentiment(texts)
    
    for t, r in zip(tweets, results):
        t["sentiment"] = r["label"]
        t["score"] = r["score"]

    logger.info("[Step 4]: Alerting if negative sentiment ratio is high")
    negative_count = sum(1 for t in tweets if t.get("sentiment", "").lower() == "negative")
    if negative_count / len(tweets) > PIPELINE_SENTIMENT_THRESHOLD:
        logger.warning(f"High negative sentiment detected: {negative_count}/{len(tweets)}")
        send_email_alert(f"⚠️ Alert: {negative_count}/{len(tweets)} recent mentions are negative!")
        logger.info("Alert email sent.")

    for t in tweets:
        logger.info(t)


if __name__ == "__main__":
    run_pipeline()