# src/logger_setup.py
import logging
import sys

def setup_logger():
    """Sets up the root logger to log to file and console."""
    
    # Configure logging to write to 'bot.log'
    # This meets the requirement for a structured log file
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("bot.log"),  # Output to bot.log 
            logging.StreamHandler(sys.stdout)  # Output to console
        ]
    )
    logger = logging.getLogger(__name__)
    return logger

# Create a global logger instance that can be imported
logger = setup_logger()
