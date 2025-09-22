import os
import tweepy
from dotenv import load_dotenv


# Load variables from .env.local
load_dotenv(".env.local")


def get_twitter_client():
    """Initialize and return Twitter client"""
    return tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))


def fetch_keyword_tweets(query: str, max_results: int, logger) -> list:
    """Fetch recent tweets for a given keyword query"""
    logger.info(f" [*] Fetching tweets for keyword: {query}")
    client = get_twitter_client()

    tweets = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        tweet_fields=["created_at", "lang"]
    )

    results = []
    if tweets.data:
        for tweet in tweets.data:
            results.append({
                "source": "twitter",
                "type": "keyword",
                "query": query,
                "text": tweet.text,
                "timestamp": tweet.created_at.isoformat()
            })
    return results

def fetch_user_tweets(user_handle: str, max_results: int, logger) -> list:
    """Fetch recent tweets for a specific user handle"""
    logger.info(f" [*] Fetching tweets for user: {user_handle}")
    client = get_twitter_client()

    try:
        user = client.get_user(username=user_handle)
        if not user.data:
            logger.warning(f"User not found: {user_handle}")
            return []
        
        user_id = user.data.id
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            tweet_fields=["created_at", "lang"]
        )
    except Exception as e:
        logger.error(f"Error fetching tweets for {user_handle}: {e}")
        return []

    results = []
    if tweets.data:
        for tweet in tweets.data:
            results.append({
                "source": "twitter",
                "type": "user",
                "user": user_handle,
                "text": tweet.text,
                "timestamp": tweet.created_at.isoformat()
            })
    return results