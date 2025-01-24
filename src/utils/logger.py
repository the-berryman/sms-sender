# src/utils/logger.py
"""
A centralized logging utility for the SMS Sender application.
This module provides a single source of truth for all logging operations,
preventing duplicate logs and ensuring consistent log formatting.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler


class SingletonLogger:
    """
    A singleton class to ensure we only ever have one logger instance.
    This prevents duplicate logging by maintaining a single source of truth.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once, even if multiple instances are created
        if not SingletonLogger._initialized:
            self.logger = self._configure_logger()
            SingletonLogger._initialized = True

    def _configure_logger(self):
        """
        Configure the logger with both file and console handlers.
        Returns a configured logger instance with proper formatting and handlers.
        """
        # Create logger
        logger = logging.getLogger('sms_sender')
        logger.setLevel(logging.DEBUG)

        # Clear any existing handlers to prevent duplicates
        logger.handlers = []

        # Prevent propagation to root logger to avoid duplicate logs
        logger.propagate = False

        # Create logs directory if it doesn't exist
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s\n'
            'Additional Info:\n'
            '%(details)s\n'
            '-' if '%(details)s' != '' else ''
        )

        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        # Create and configure file handler with rotation
        file_handler = RotatingFileHandler(
            logs_dir / f'sms_sender.log',
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)

        # Create and configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def log_api_interaction(self, direction, payload, additional_info=None):
        """
        Log API interactions with proper formatting.

        Args:
            direction: 'SENT' or 'RECEIVED'
            payload: The payload to log
            additional_info: Any additional information to include
        """
        message = f"API {direction} - {datetime.now().isoformat()}"
        details = f"Payload:\n{payload}"

        if additional_info:
            details += f"\n\nAdditional Information:\n{additional_info}"
        else:
            details = ""

        self.logger.info(message, extra={'details': details})

    def info(self, message, details=""):
        """Log an info message with optional details"""
        self.logger.info(message, extra={'details': details})

    def error(self, message, details="", exc_info=None):
        """Log an error message with optional details and exception info"""
        self.logger.error(message, extra={'details': details}, exc_info=exc_info)

    def debug(self, message, details=""):
        """Log a debug message with optional details"""
        self.logger.debug(message, extra={'details': details})


# Create a global logger instance
logger = SingletonLogger()

# Export only the logger instance
__all__ = ['logger']