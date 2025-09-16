import os
import traceback

from utils.config import CONFIG
from utils.logger import setup_logger

from slisten_pipeline.stage_01 import run_pipeline


# configs
LOG_PATH = CONFIG["LOG_PATH"]
MAX_RESULTS = CONFIG["MAX_RESULTS"]
PIPELINE_SENTIMENT_THRESHOLD = CONFIG["PIPELINE_SENTIMENT_THRESHOLD"]
RESULTS_DIR = CONFIG["RESULTS_DIR"]

# setup logger
LOG_DIR = os.path.join(os.getcwd(), LOG_PATH)
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "main.log")


def main():
    logger = setup_logger("main_logger", LOG_FILE)
    try:
        logger.info(" ")
        logger.info("////--//--//----STARTING [PIPELINE 01] SOCIAL LISTENING PIPELINE----//--//--////")
        
        try:
            logger.info(" ")
            logger.info("----------STARTING [STAGE 01]----------")
            run_pipeline(MAX_RESULTS, PIPELINE_SENTIMENT_THRESHOLD, RESULTS_DIR, logger)
            # logger.info("Already Done. Skipping...")
            logger.info("----------FINISHED [STAGE 01]----------")
            logger.info(" ")
        except Exception as e:
            logger.error(f"ERROR RUNNING [STAGE 01]: {e}")
            logger.debug(traceback.format_exc())
            return

        logger.info("////--//--//----FINISHED [PIPELINE 01] SOCIAL LISTENING PIPELINE----//--//--////")
        logger.info(" ")
    except Exception as e:
        logger.error(f"ERROR RUNNING [PIPELINE 01] SOCIAL LISTENING PIPELINE: {e}")
        logger.debug(traceback.format_exc())
        return


if __name__ == "__main__":
    main()