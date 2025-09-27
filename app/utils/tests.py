"""Smoke tests for utils module."""

import os
import sys
from unittest.mock import patch, MagicMock
from django.test import TestCase


class UtilsTests(TestCase):
    """Basic smoke tests for utils functionality."""

    def test_utils_imports(self):
        """Test that utils modules can be imported."""
        try:
            from utils import conf, util, logger  # noqa: F401
        except Exception as e:
            self.fail(f"Failed to import utils modules: {e}")

    def test_conf_settings_manager(self):
        """Test that SettingsManager can be instantiated."""
        try:
            from utils.conf import settings_manager

            self.assertIsNotNone(settings_manager)
        except Exception as e:
            self.fail(f"Failed to test SettingsManager: {e}")

    def test_logger_import(self):
        """Test that logger module imports correctly."""
        try:
            from utils.logger import log

            self.assertIsNotNone(log)
        except Exception as e:
            self.fail(f"Failed to import logger: {e}")


class RollbarIntegrationTests(TestCase):
    """Tests for rollbar integration."""

    def test_rollbar_config_import(self):
        """Test that rollbar config can be imported."""
        try:
            from utils.rollbar_config import (
                init_rollbar,
                report_exception,
                report_message,
            )

            self.assertIsNotNone(init_rollbar)
            self.assertIsNotNone(report_exception)
            self.assertIsNotNone(report_message)
        except Exception as e:
            self.fail(f"Failed to import rollbar config: {e}")

    def test_logger_with_rollbar_functions(self):
        """Test that logger functions work with rollbar integration."""
        try:
            from utils.logger import log, log_exception

            # Test basic logging
            log("Test info message", 0)
            log("Test warning message", 1)
            log("Test error message", 2)

            # Test exception logging
            try:
                raise ValueError("Test exception")
            except Exception:
                log_exception(sys.exc_info(), {"test": "data"})

        except Exception as e:
            self.fail(f"Logger with rollbar integration failed: {e}")

    @patch.dict(os.environ, {"ROLLBAR_TOKEN": "test_token"})
    @patch("utils.rollbar_config.rollbar")
    def test_rollbar_initialization(self, mock_rollbar):
        """Test rollbar initialization when token is present."""
        from utils.rollbar_config import init_rollbar

        # Mock rollbar.init to avoid actual initialization
        mock_rollbar.init = MagicMock()

        result = init_rollbar()
        self.assertTrue(result)
        mock_rollbar.init.assert_called_once()

    def test_rollbar_initialization_without_token(self):
        """Test rollbar initialization when token is not present."""
        # Ensure no ROLLBAR_TOKEN is set
        with patch.dict(os.environ, {}, clear=True):
            from utils.rollbar_config import init_rollbar

            result = init_rollbar()
            self.assertFalse(result)

    @patch.dict(os.environ, {"ROLLBAR_TOKEN": "test_token"})
    @patch("utils.rollbar_config.rollbar")
    def test_report_exception(self, mock_rollbar):
        """Test exception reporting to rollbar."""
        from utils.rollbar_config import report_exception

        # Mock rollbar.report_exc_info
        mock_rollbar.report_exc_info = MagicMock()

        try:
            raise RuntimeError("Test exception")
        except Exception:
            report_exception(sys.exc_info(), {"context": "test"})

        mock_rollbar.report_exc_info.assert_called_once()

    @patch.dict(os.environ, {"ROLLBAR_TOKEN": "test_token"})
    @patch("utils.rollbar_config.rollbar")
    def test_report_message(self, mock_rollbar):
        """Test message reporting to rollbar."""
        from utils.rollbar_config import report_message

        # Mock rollbar.report_message
        mock_rollbar.report_message = MagicMock()

        report_message("Test message", "error", {"extra": "data"})

        mock_rollbar.report_message.assert_called_once_with(
            "Test message", level="error", extra_data={"extra": "data"}
        )
