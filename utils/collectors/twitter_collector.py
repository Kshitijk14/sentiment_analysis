import tweepy
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def fetch_tweets(query, max_results=20):
    """Fetch recent tweets for a given query"""
    config = load_config()
    client = tweepy.Client(bearer_token=config["twitter"]["bearer_token"])
    
    tweets = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["created_at", "lang"])
    
    results = []
    if tweets.data:
        for tweet in tweets.data:
            results.append({
                "source": "twitter",
                "text": tweet.text,
                "timestamp": tweet.created_at.isoformat()
            })
    return results
