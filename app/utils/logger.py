import typing
import os
import logging

# Set up default logger
logger = logging.getLogger(__name__)


def log(message: str, level: typing.Optional[int] = 0):
    """
    Log a message with optional rollbar integration.

    Args:
        message: The message to log
        level: Log level (0=INFO, 1=WARNING, 2=ERROR)
    """
    # Map level to logging levels
    level_map = {
        0: logging.INFO,
        1: logging.WARNING,
        2: logging.ERROR,
    }

    # Log to standard Python logging
    log_level = level_map.get(level, logging.INFO)
    logger.log(log_level, message)

    # If rollbar is configured, also log to rollbar for warnings and errors
    if level >= 1 and os.getenv("ROLLBAR_TOKEN"):
        try:
            from .rollbar_config import report_message

            if level == 1:
                report_message(message, "warning")
            elif level >= 2:
                report_message(message, "error")
        except ImportError:
            # Rollbar not available, continue with standard logging
            pass


def log_exception(exc_info=None, extra_data=None):
    """
    Log an exception to rollbar with full context.

    Args:
        exc_info: Exception info tuple (type, value, traceback)
        extra_data: Additional context data to include
    """
    if os.getenv("ROLLBAR_TOKEN"):
        try:
            from .rollbar_config import report_exception

            report_exception(exc_info=exc_info, extra_data=extra_data)
        except ImportError:
            # Rollbar not available, fall back to standard logging
            logger.exception("Exception occurred", exc_info=exc_info)
    else:
        # No rollbar token, use standard logging
        logger.exception("Exception occurred", exc_info=exc_info)
