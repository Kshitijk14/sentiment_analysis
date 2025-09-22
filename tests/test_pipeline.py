import pytest
import os
import pandas as pd
from unittest.mock import patch

from slisten_pipeline.stage_01 import run_pipeline
from utils.logger import setup_logger


# Fixtures
@pytest.fixture
def logger(tmp_path):
    log_file = tmp_path / "test.log"
    return setup_logger("test_logger", log_file)


@pytest.fixture
def results_dir(tmp_path):
    path = tmp_path / "results"
    os.makedirs(path, exist_ok=True)
    return str(path)


# Mock tweets
mock_user_tweets = [
    {"source": "twitter", "type": "user", "user": "elonmusk", "text": "Tesla is amazing!", "timestamp": "2025-09-19T12:00:00"}
]

mock_keyword_tweets = [
    {"source": "twitter", "type": "keyword", "query": "Samsung", "text": "Samsung phones are bad.", "timestamp": "2025-09-19T13:00:00"}
]

# Mock Config
mock_config = {
    "twitter": {"watchlist_users": ["user1"], "keywords": ["test"]}
}

# Tests
def test_pipeline_with_mocked_collectors(logger, results_dir):
    with patch("slisten_pipeline.stage_01.fetch_user_tweets", return_value=mock_user_tweets), \
         patch("slisten_pipeline.stage_01.fetch_keyword_tweets", return_value=mock_keyword_tweets), \
         patch("slisten_pipeline.stage_01.send_email_alert", return_value=None):

        run_pipeline(max_results=10, pipeline_sentiment_threshold=0.3, results_dir=results_dir, logger=logger, config=mock_config)

        # Check if CSV was created
        csv_path = os.path.join(results_dir, "tweets_results.csv")
        assert os.path.exists(csv_path)

        # Check content
        df = pd.read_csv(csv_path)
        assert "cleaned_text" in df.columns
        assert "sentiment" in df.columns
        assert len(df) >= 2  # one user tweet + one keyword tweet
