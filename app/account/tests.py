"""Smoke tests for account app."""

from django.test import TestCase
from django.contrib.auth.models import User


class AccountAppTests(TestCase):
    """Basic smoke tests for account app functionality."""

    def test_account_app_loading(self):
        """Test that account app loads without errors."""
        from account import models, views

        self.assertIsNotNone(models)
        self.assertIsNotNone(views)

    def test_account_models_import(self):
        """Test that account models can be imported."""
        try:
            import account.models  # noqa: F401
        except Exception as e:
            self.fail(f"Failed to import account models: {e}")

    def test_account_views_import(self):
        """Test that account views can be imported."""
        try:
            import account.views  # noqa: F401
        except Exception as e:
            self.fail(f"Failed to import account views: {e}")

    def test_user_model_creation(self):
        """Test basic user model functionality."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
