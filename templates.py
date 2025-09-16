import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


project_name = "social_listening"

list_of_files = [
    "artifacts/data/.gitkeep",
    "artifacts/summaries/.gitkeep",
    "artifacts/results/.gitkeep",

    # pipeline
    "rag_pipeline/__init__.py",
    "rag_pipeline/stage_01_data_prep.py",
    "rag_pipeline/stage_02_populate_vector_db.py",
    "rag_pipeline/stage_03_query_workflow.py",

    # utils
    "utils/__init__.py",
    "utils/config.py",
    "utils/logger.py",
    
    "utils/helpers/__init__.py",
    "utils/helpers/common.py",
    "utils/helpers/email_alerts.py",
    
    # preprocessing
    "utils/preprocessing/__init__.py",
    "utils/preprocessing/text_cleaner.py",
    
    # collectors
    "utils/collectors/__init__.py",
    "utils/collectors/twitter_collector.py",
    "utils/collectors/reddit_collector.py",
    "utils/collectors/facebook_collector.py",
    "utils/collectors/youtube_collector.py",
    "utils/collectors/instagram_collector.py",
    "utils/collectors/newsapi_collector.py",
    "utils/collectors/web_scraper.py",
    
    # models
    "utils/models/__init__.py",
    "utils/models/sentiment_analyzer.py",

    # tests
    "tests/__init__.py",
    
    # docs
    "docs/README.md",
    "docs/REFERENCE.md",
    "docs/ARCHITECTURE.md",
    "docs/INSTALLATION.md",
    "docs/CONTRIBUTING.md",

    "params.yaml",
    "dvc.yaml",
    ".env.local",
    ".env.example",
]


for filepath in list_of_files:
    filepath = Path(filepath) #to solve the windows path issue
    filedir, filename = os.path.split(filepath) # to handle the project_name folder


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")