"""
Django management command to test rollbar integration.
"""

import sys
from django.core.management.base import BaseCommand
from utils.logger import log, log_exception
from utils.rollbar_config import report_message, report_exception


class Command(BaseCommand):
    help = "Test rollbar integration"

    def add_arguments(self, parser):
        parser.add_argument(
            "--test-exception",
            action="store_true",
            help="Test exception reporting",
        )
        parser.add_argument(
            "--test-message",
            action="store_true",
            help="Test message reporting",
        )

    def handle(self, *args, **options):
        self.stdout.write("Testing rollbar integration...")

        # Test basic logging
        log("Management command: Info message", 0)
        log("Management command: Warning message", 1)
        log("Management command: Error message", 2)

        # Test direct rollbar calls
        report_message("Management command: Direct rollbar message", "info")

        if options["test_exception"]:
            self.stdout.write("Testing exception handling...")
            try:
                raise ValueError("Test exception from management command")
            except Exception:
                log_exception(sys.exc_info(), {"context": "management_command"})
                report_exception(sys.exc_info(), {"source": "test_command"})

        if options["test_message"]:
            self.stdout.write("Testing message reporting...")
            report_message("Test message from management command", "warning")

        self.stdout.write(
            self.style.SUCCESS("Rollbar integration test completed successfully!")
        )
