"""
Test script to verify rollbar integration works correctly.
"""
import os
import sys
from .logger import log, log_exception
from .rollbar_config import report_message, report_exception


def test_rollbar_integration():
    """Test rollbar integration without requiring actual rollbar token."""
    print("Testing rollbar integration...")
    
    # Test basic logging
    print("Testing basic logging functions...")
    log("Test info message", 0)
    log("Test warning message", 1)
    log("Test error message", 2)
    
    # Test exception logging
    print("Testing exception logging...")
    try:
        raise ValueError("Test exception for rollbar")
    except Exception:
        log_exception(sys.exc_info(), {"test_data": "rollbar_test"})
    
    print("Rollbar integration test completed successfully!")
    
    # Test rollbar functions directly
    print("Testing rollbar functions...")
    report_message("Test rollbar message", "info")
    
    try:
        raise RuntimeError("Test runtime error")
    except Exception:
        report_exception(sys.exc_info(), {"context": "direct_test"})
    
    print("All rollbar tests completed!")


if __name__ == "__main__":
    test_rollbar_integration()