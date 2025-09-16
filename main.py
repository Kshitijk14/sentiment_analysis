from collectors.twitter_collector import fetch_tweets
from preprocessing.text_cleaner import clean_text
from sentiment.sentiment_analyzer import analyze_sentiment
from alerts.email import send_email_alert
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def run_pipeline():
    config = load_config()
    
    # Step 1: Collect data from Twitter
    tweets = fetch_tweets("Samsung", max_results=15)
    
    if not tweets:
        print("No tweets found for this query.")
        return
    
    # Step 2: Preprocess
    for t in tweets:
        t["cleaned_text"] = clean_text(t["text"])
    
    # Step 3: Sentiment Analysis
    texts = [t["cleaned_text"] for t in tweets if t["cleaned_text"]]
    results = analyze_sentiment(texts)
    
    for t, r in zip(tweets, results):
        t["sentiment"] = r["label"]
        t["score"] = r["score"]
    
    # Step 4: Alerting if negative sentiment ratio is high
    negative_count = sum(1 for t in tweets if t.get("sentiment", "").lower() == "negative")
    if negative_count / len(tweets) > config["pipeline"]["sentiment_threshold"]:
        send_email_alert(f"⚠️ Alert: {negative_count}/{len(tweets)} recent mentions are negative!")
    
    # Print results
    for t in tweets:
        print(t)

if __name__ == "__main__":
    run_pipeline()
