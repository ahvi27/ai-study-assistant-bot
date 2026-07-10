"""
Logging utility module for Study Assistant Bot.
Configures logging for the application.
"""

import logging
import sys
from pathlib import Path
from config import Config

# Create logs directory
logs_dir = Path(Config.LOG_FILE).parent
logs_dir.mkdir(parents=True, exist_ok=True)


def setup_logging():
    """Configure logging for the application."""
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(Config.LOG_LEVEL)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(Config.LOG_FILE)
    file_handler.setLevel(Config.LOG_LEVEL)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    return root_logger


# Initialize logging
logger = setup_logging()


def get_logger(name: str) -> logging.Logger:
    """Get logger for module."""
    return logging.getLogger(name)
