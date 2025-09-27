"""Smoke tests for core app."""

from django.test import TestCase


class CoreAppTests(TestCase):
    """Basic smoke tests for core app functionality."""

    def test_core_app_loading(self):
        """Test that core app loads without errors."""
        from core import models, views

        self.assertIsNotNone(models)
        self.assertIsNotNone(views)

    def test_core_models_import(self):
        """Test that core models can be imported."""
        try:
            import core.models  # noqa: F401
        except Exception as e:
            self.fail(f"Failed to import core models: {e}")

    def test_core_views_import(self):
        """Test that core views can be imported."""
        try:
            import core.views  # noqa: F401
        except Exception as e:
            self.fail(f"Failed to import core views: {e}")
