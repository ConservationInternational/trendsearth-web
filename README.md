# trendsearth-web

Django web application for Trends.Earth platform, providing a user-friendly interface for monitoring land degradation and environmental indicators.

## Features

- Django-based web application with geospatial capabilities
- Integration with Trends.Earth API
- PostGIS database support
- Comprehensive exception logging with Rollbar integration

## Exception Logging

This application includes comprehensive exception logging through Rollbar integration. All uncaught exceptions are automatically captured and sent to Rollbar with full context.

### Configuration

To enable Rollbar exception logging, set the following environment variables:

```bash
# Required: Your Rollbar access token
ROLLBAR_TOKEN=your_rollbar_token_here

# Optional: Environment name (defaults to "development")
ROLLBAR_ENVIRONMENT=production
```

### Usage

The application automatically captures:
- All uncaught exceptions through Django middleware
- Manual log messages with warning/error levels
- Exception context and user information

#### Programmatic Usage

```python
from utils.logger import log, log_exception
from utils.rollbar_config import report_message, report_exception

# Log messages (automatically sent to Rollbar for warnings/errors)
log("Info message", 0)      # INFO level
log("Warning message", 1)   # WARNING level 
log("Error message", 2)     # ERROR level

# Log exceptions with context
try:
    # some code that might fail
    pass
except Exception:
    log_exception(sys.exc_info(), {"context": "additional_data"})

# Direct Rollbar reporting
report_message("Custom message", "error")
report_exception(sys.exc_info(), {"custom": "context"})
```

### Testing

Test the rollbar integration using the management command:

```bash
python manage.py test_rollbar
python manage.py test_rollbar --test-exception
python manage.py test_rollbar --test-message
```
