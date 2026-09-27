"""Logging setup for Console and JSON logging."""

import logging
import json
import sys

def setup_logging(verbose: bool = False, quiet: bool = False, json_log: bool = False):
    """Configure logger with clean console output or JSON lines."""
    level = logging.INFO
    if verbose:
        level = logging.DEBUG
    elif quiet:
        level = logging.ERROR

    logger = logging.getLogger("dw_agent")
    logger.setLevel(level)
    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    if json_log:
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                return json.dumps({
                    "timestamp": self.formatTime(record),
                    "level": record.levelname,
                    "message": record.getMessage()
                })
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(handler)
    return logger

def get_logger():
    return logging.getLogger("dw_agent")
