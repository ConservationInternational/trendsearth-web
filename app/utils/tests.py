"""Smoke tests for utils module."""

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
