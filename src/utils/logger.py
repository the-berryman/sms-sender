# src/utils/logger.py
"""
Logging utility for the SMS Sender application.
This module configures logging to both file and console with proper formatting.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger():
    """
    Configure and return a logger that writes to both file and console.
    The file logs will be stored in a 'logs' directory with the current date.
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)

    # Create a logger
    logger = logging.getLogger('sms_sender')
    logger.setLevel(logging.DEBUG)

    # Create formatters for different levels of detail
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s\n'
        'Additional Info:\n'
        '%(details)s\n'
        '-' * 80
    )

    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # Create and configure file handler for detailed logging
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(
        logs_dir / f'sms_sender_{current_date}.log',
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Create and configure console handler for basic logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_api_interaction(logger, direction, payload, additional_info=None):
    """
    Log API interactions with proper formatting.

    Args:
        logger: The logger instance to use
        direction: 'SENT' or 'RECEIVED'
        payload: The payload to log
        additional_info: Any additional information to include
    """
    message = f"API {direction} - {datetime.now().isoformat()}"
    details = f"Payload:\n{payload}"

    if additional_info:
        details += f"\nAdditional Information:\n{additional_info}"

    # Use the custom formatter by passing details as extra
    logger.info(message, extra={'details': details})