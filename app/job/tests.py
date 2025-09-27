"""Smoke tests for job app."""

from django.test import TestCase


class JobAppTests(TestCase):
    """Basic smoke tests for job app functionality."""

    def test_job_app_loading(self):
        """Test that job app loads without errors."""
        from job import models, views

        self.assertIsNotNone(models)
        self.assertIsNotNone(views)

    def test_job_models_import(self):
        """Test that job models can be imported."""
        try:
            from job.models import Job, Status, Layer  # noqa: F401
        except Exception as e:
            self.fail(f"Failed to import job models: {e}")

    def test_job_views_import(self):
        """Test that job views can be imported."""
        try:
            import job.views  # noqa: F401
        except Exception as e:
            self.fail(f"Failed to import job views: {e}")
