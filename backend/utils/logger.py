"""
PainToAd AI - Centralized Logging Utility
=========================================
Provides structured, thread-safe, production-ready logging with console coloring,
log formatting, and environment-aware log level configurations.
"""

import sys
import logging
from typing import Optional
from backend.config.settings import settings


class CustomFormatter(logging.Formatter):
    """
    Custom ANSI color-coded log formatter for terminal output in development/production.
    """
    grey = "\x1b[38;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: blue + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, self.format_str)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logging(name: Optional[str] = "pain_to_ad_ai") -> logging.Logger:
    """
    Configures and returns a centralized Logger instance.
    """
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(log_level)

    # Avoid duplicate handlers if already configured
    if not logger_instance.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(CustomFormatter())
        logger_instance.addHandler(console_handler)

    logger_instance.propagate = False
    return logger_instance


# Export global singleton logger
logger = setup_logging()
