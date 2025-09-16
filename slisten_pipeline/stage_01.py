import traceback
import pandas as pd

from utils.collectors.twitter_collector import fetch_tweets
from utils.preprocessing.text_cleaner import clean_text
from utils.models.sentiment_analyzer import analyze_sentiment
from utils.helpers.email_alerts import send_email_alert


def run_pipeline(max_results, pipeline_sentiment_threshold, results_dir, logger):    
    try:
        logger.info("[STAGE 01] [Step 1]: Collect data from Twitter")
        tweets = fetch_tweets("Samsung", max_results, logger)
        
        if not tweets:
            logger.warning("No tweets found for this query.")
            return
    except Exception as e:
        logger.error(f"[STAGE 01] [Step 1]: Error fetching tweets: {e}")
        logger.debug(traceback.format_exc())
        return

    try:
        logger.info("[STAGE 01] [Step 2]: Preprocess")
        for t in tweets:
            t["cleaned_text"] = clean_text(t["text"], logger)
            logger.debug(f"Original: {t['text']}\nCleaned: {t['cleaned_text']}\n")
    except Exception as e:
        logger.error(f"[STAGE 01] [Step 2]: Error in preprocessing: {e}")
        logger.debug(traceback.format_exc())
        return

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

    try:
        logger.info("[STAGE 01] [Step 4]: Alerting if negative sentiment ratio is high")
        negative_count = sum(1 for t in tweets if t.get("sentiment", "").lower() == "negative")
        
        if negative_count / len(tweets) > pipeline_sentiment_threshold:
            logger.warning(f"High negative sentiment detected: {negative_count}/{len(tweets)}")
            
            send_email_alert(f"[Alert] High negative sentiment detected: {negative_count}/{len(tweets)} recent mentions are negative!")
            logger.info("Alert email sent.")
    except Exception as e:
        logger.error(f"[STAGE 01] [Step 4]: Error in alerting: {e}")
        logger.debug(traceback.format_exc())
        return

    try:
        logger.info("[STAGE 01] [Step 5]: Saving results to CSV")
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