"""
Rollbar configuration and initialization for Trends.Earth web application.
"""

import os
import rollbar
from django.conf import settings


def init_rollbar():
    """Initialize rollbar if token is provided."""
    rollbar_token = os.getenv("ROLLBAR_TOKEN")
    if rollbar_token:
        rollbar.init(
            access_token=rollbar_token,
            environment=os.getenv("ROLLBAR_ENVIRONMENT", "development"),
            root=settings.BASE_DIR,
            code_version="1.0",
            capture_username=True,
            capture_ip=True,
            capture_email=True,
            locals={
                "enabled": True,
            },
            exception_level_filters=[
                (KeyboardInterrupt, "ignored"),
            ],
            branch="main",
        )
        return True
    return False


def report_exception(exc_info=None, extra_data=None, level="error"):
    """Report an exception to rollbar with full context."""
    if os.getenv("ROLLBAR_TOKEN"):
        try:
            rollbar.report_exc_info(
                exc_info=exc_info, extra_data=extra_data, level=level
            )
        except Exception:
            # If rollbar fails, don't crash the application
            pass


def report_message(message, level="info", extra_data=None):
    """Report a message to rollbar."""
    if os.getenv("ROLLBAR_TOKEN"):
        try:
            rollbar.report_message(message, level=level, extra_data=extra_data)
        except Exception:
            # If rollbar fails, don't crash the application
            pass
