import os
import tweepy
from dotenv import load_dotenv


# Load variables from .env.local
load_dotenv(".env.local")


def fetch_tweets(query: str, max_results: int, logger) -> dict:
    """Fetch recent tweets for a given query"""
    logger.info(" [*] Setting up Twitter client...")
    client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

    logger.info(" [*] Fetching tweets...")
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
