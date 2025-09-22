import traceback
import pandas as pd

from utils.collectors.twitter_collector import fetch_user_tweets, fetch_keyword_tweets
from utils.preprocessing.text_cleaner import clean_text
from utils.models.sentiment_analyzer import analyze_sentiment
from utils.helpers.email_alerts import send_email_alert
from utils.config import CONFIG

def run_pipeline(max_results, pipeline_sentiment_threshold, results_dir, logger, config=None):
    tweets = []
    if config is None:
        config = CONFIG    

    # ------------------------------
    # Step 1: Collect data
    # ------------------------------
    try:
        logger.info("[STAGE 01] [Step 1]: Collecting tweets from keywords and users")

        # From watchlist users
        for user in CONFIG.get("WATCHLIST_USERS", []):
            user_tweets = fetch_user_tweets(user, max_results, logger)
            tweets.extend(user_tweets)

        # From keywords
        for keyword in CONFIG.get("KEYWORDS", []):
            keyword_tweets = fetch_keyword_tweets(keyword, max_results, logger)
            tweets.extend(keyword_tweets)

        if not tweets:
            logger.warning("No tweets found for this run.")
            return
    except Exception as e:
        logger.error(f"[STAGE 01] [Step 1]: Error fetching tweets: {e}")
        logger.debug(traceback.format_exc())
        return

    # ------------------------------
    # Step 2: Preprocess
    # ------------------------------
    try:
        logger.info("[STAGE 01] [Step 2]: Preprocessing tweets")
        for t in tweets:
            t["cleaned_text"] = clean_text(t["text"], logger)
            logger.debug(f"Original: {t['text']}\nCleaned: {t['cleaned_text']}\n")
    except Exception as e:
        logger.error(f"[STAGE 01] [Step 2]: Error in preprocessing: {e}")
        logger.debug(traceback.format_exc())
        return

    # ------------------------------
    # Step 3: Sentiment Analysis
    # ------------------------------
    try:
        logger.info("[STAGE 01] [Step 3]: Sentiment Analysis")
        texts = [t["cleaned_text"] for t in tweets if t["cleaned_text"]]
        results = analyze_sentiment(texts)

        if not results:
            logger.warning("Sentiment analysis returned no results.")
            return

        for t, r in zip(tweets, results):
            t["sentiment"] = r["label"]
            t["score"] = r["score"]
    except Exception as e:
        logger.error(f"[STAGE 01] [Step 3]: Error in sentiment analysis: {e}")
        logger.debug(traceback.format_exc())
        return

    # ------------------------------
    # Step 4: Alerting
    # ------------------------------
    try:
        logger.info("[STAGE 01] [Step 4]: Alerting based on sentiment thresholds")

        negative_count = sum(1 for t in tweets if t.get("sentiment", "").lower() == "negative")
        if negative_count / len(tweets) > pipeline_sentiment_threshold:
            logger.warning(f"High negative sentiment detected: {negative_count}/{len(tweets)}")
            send_email_alert(
                "[Alert] High negative sentiment detected",
                f"{negative_count}/{len(tweets)} recent mentions are negative!"
            )
            logger.info("Alert email sent.")
    except Exception as e:
        logger.error(f"[STAGE 01] [Step 4]: Error in alerting: {e}")
        logger.debug(traceback.format_exc())
        return

    # ------------------------------
    # Step 5: Save Results
    # ------------------------------
    try:
        logger.info("[STAGE 01] [Step 5]: Saving results to CSV")
        for t in tweets:
            t["keywords_used"] = ",".join(config.get("KEYWORDS", []))
            t["user_ids_used"] = ",".join(config.get("USER_IDS", []))
            
        df = pd.DataFrame(tweets)
        csv_results_path = f"{results_dir}/tweets_results.csv"
        df.to_csv(csv_results_path, index=False, encoding="utf-8")
        logger.info(f"Saved {len(tweets)} tweets to {csv_results_path}")
    except Exception as e:
        logger.error(f"[STAGE 01] [Step 5]: Error saving to CSV: {e}")
        logger.debug(traceback.format_exc())
        return

    for t in tweets:
        logger.info(t)


if __name__ == "__main__":
    run_pipeline()