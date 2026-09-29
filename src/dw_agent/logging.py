# Module docstring explaining logging configuration for console and JSON structured log output
"""Logging setup module supporting clean text console formatting or structured JSON lines."""

# Import Python standard logging module
import logging
# Import json module for serializing log records into JSON formatted lines
import json
# Import sys module to route logs to stdout stream
import sys

# Function configuring logger with verbosity flags and optional JSON output format
def setup_logging(verbose: bool = False, quiet: bool = False, json_log: bool = False):
    """Configure dw_agent logger with text or JSON line output stream handlers.

    Args:
        verbose (bool): If True, sets logging level to DEBUG for detailed output.
        quiet (bool): If True, sets logging level to ERROR to suppress info logs.
        json_log (bool): If True, formats output log messages as structured JSON objects.

    Returns:
        logging.Logger: Configured logger instance named 'dw_agent'.
    """
    # Default log level is INFO
    level = logging.INFO
    # Set DEBUG level if verbose flag is enabled
    if verbose:
        level = logging.DEBUG
    # Set ERROR level if quiet flag is enabled
    elif quiet:
        level = logging.ERROR

    # Get dw_agent logger instance
    logger = logging.getLogger("dw_agent")
    # Apply configured logging severity threshold
    logger.setLevel(level)
    # Clear any existing handlers to prevent duplicate output
    logger.handlers.clear()

    # Create stdout stream handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Apply custom JSON formatter if json_log flag is active
    if json_log:
        class JsonFormatter(logging.Formatter):
            """Custom logging formatter serializing records into JSON lines."""
            def format(self, record):
                return json.dumps({
                    "timestamp": self.formatTime(record),
                    "level": record.levelname,
                    "message": record.getMessage()
                })
        handler.setFormatter(JsonFormatter())
    else:
        # Simple plain message console formatting for clean terminal readability
        handler.setFormatter(logging.Formatter("%(message)s"))

    # Attach configured stream handler to logger
    logger.addHandler(handler)
    return logger

# Function returning existing 'dw_agent' logger instance
def get_logger():
    """Retrieve the global 'dw_agent' logger instance.

    Returns:
        logging.Logger: System logger instance.
    """
    return logging.getLogger("dw_agent")

