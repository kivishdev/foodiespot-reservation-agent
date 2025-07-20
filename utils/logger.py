import logging
import os

def setup_logger():
    """Setup basic logger"""
    logger = logging.getLogger("foodiespot")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def log_message(message):
    """Log info message"""
    logger = setup_logger()
    logger.info(message)

def log_error(error_message):
    """Log error message"""
    logger = setup_logger()
    logger.error(f"ERROR: {error_message}")
