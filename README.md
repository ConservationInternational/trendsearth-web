# Trends.Earth Web

[![Trends.Earth](https://s3.amazonaws.com/trends.earth/sharing/trends_earth_logo_bl_600width.png)](http://trends.earth)

[![Testing](https://github.com/ConservationInternational/trendsearth-web/actions/workflows/testing.yml/badge.svg)](https://github.com/ConservationInternational/trendsearth-web/actions/workflows/testing.yml)
[![Code Quality](https://github.com/ConservationInternational/trendsearth-web/actions/workflows/code-quality.yml/badge.svg)](https://github.com/ConservationInternational/trendsearth-web/actions/workflows/code-quality.yml)

Django web application for the Trends.Earth platform, providing a user-friendly interface for monitoring land degradation and environmental indicators using satellite data and Earth observation algorithms.

## Overview

Trends.Earth Web is a Django-based web application that serves as the frontend interface for [Trends.Earth](https://trends.earth), a platform for monitoring land change including productivity, land cover, and soil organic carbon. The application provides:

- **Land Degradation Monitoring**: Tools for assessing and monitoring land degradation using satellite data
- **SDG 15.3.1 Reporting**: Support for Sustainable Development Goal target 15.3 (Land Degradation Neutrality) reporting
- **Earth Observation Algorithms**: Integration with Google Earth Engine and other remote sensing platforms
- **Geospatial Analysis**: Built-in support for spatial data processing and visualization
- **User Management**: Multi-user support with geographic boundary management
- **Job Processing**: Asynchronous processing of large-scale Earth observation tasks

The application integrates with the broader [Trends.Earth ecosystem](https://trends.earth) to support monitoring land degradation for reporting to the Global Environment Facility (GEF) and United Nations Convention to Combat Desertification (UNCCD).

## Features

- **Django-based Architecture**: Modern web framework with geospatial capabilities
- **PostGIS Database**: Advanced spatial database support for geographic data
- **API Integration**: Seamless connection to Trends.Earth API services
- **Algorithm Management**: Built-in support for Earth observation processing algorithms
- **User Interface**: Bootstrap 5-based responsive design
- **Exception Logging**: Comprehensive error tracking with Rollbar integration
- **Docker Support**: Containerized deployment for easy setup and scaling

## Setup Instructions

### Prerequisites

- **Docker & Docker Compose** (recommended approach)
- **Python 3.13** (for local development)
- **PostgreSQL 15+ with PostGIS** (for local development)
- **GDAL libraries** (for geospatial operations)

### Running with Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ConservationInternational/trendsearth-web.git
   cd trendsearth-web
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and run with Docker Compose**:
   ```bash
   docker compose up --build
   ```

4. **Access the application**:
   - Web interface: http://localhost:9000
   - Database: PostgreSQL on port 5432 (internal to Docker network)

The Docker setup includes:
- **Web Application**: Django app with Gunicorn on port 9000
- **PostgreSQL Database**: PostGIS-enabled database with spatial extensions
- **Static Files**: Properly configured static file serving

### Local Development Setup

1. **Install system dependencies**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3.13 python3.13-pip postgresql-15 postgresql-15-postgis-3
   sudo apt-get install gdal-bin libgdal-dev python3-dev
   
   # macOS
   brew install python@3.13 postgresql postgis gdal
   ```

2. **Setup Python environment**:
   ```bash
   cd app/
   python3.13 -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure database**:
   ```bash
   # Create database user and database
   sudo -u postgres createuser --createdb te_user
   sudo -u postgres createdb -O te_user te_web
   sudo -u postgres psql -c "CREATE EXTENSION postgis;" te_web
   ```

4. **Run migrations and start server**:
   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:9000
   ```

## Testing

The project includes comprehensive testing at multiple levels:

### Smoke Tests

Run basic syntax and import validation:

```bash
cd app/
python test_simple.py
```

This validates:
- Python syntax across all files
- Basic Django imports
- Application directory structure

### Code Quality Checks

```bash
# Install ruff for code quality checks
pip install ruff

# Run linting
ruff check app/

# Check code formatting
ruff format --check app/
```

### Integration Tests with Docker

```bash
# Run full application stack for testing
docker compose up --build

# Run smoke tests in Docker environment
docker compose run --rm test

# Alternative: Run tests with specific profile
docker compose --profile testing run --rm test
```

### Rollbar Integration Testing

Test exception logging with the built-in management command:

```bash
python manage.py test_rollbar
python manage.py test_rollbar --test-exception
python manage.py test_rollbar --test-message
```

## Code Structure

The application follows Django's standard project structure with specialized apps for different functionality:

```
trendsearth-web/
├── .github/workflows/      # CI/CD pipelines (testing, code-quality)
├── app/                    # Main Django application
│   ├── main/              # Project settings and configuration
│   │   ├── settings.py    # Django settings, database, API config
│   │   ├── urls.py        # Root URL routing
│   │   └── wsgi.py        # WSGI application entry point
│   ├── account/           # User management and geographic data
│   │   ├── models.py      # Country, Region, City, User models
│   │   ├── configs/       # Geographic boundary data (JSON)
│   │   └── templates/     # User interface templates
│   ├── core/              # Algorithm management and UI logic
│   │   ├── models.py      # Aggregation classes, user preferences
│   │   ├── views.py       # AJAX endpoints for algorithms
│   │   └── templates/     # Algorithm interface templates
│   ├── job/               # Job execution and result management
│   │   ├── models.py      # Job, Status, Layer models
│   │   ├── views.py       # Job execution endpoints
│   │   └── templates/     # Job management interfaces
│   ├── utils/             # Utility functions and configurations
│   │   ├── conf.py        # Algorithm configurations
│   │   ├── data/          # JSON configurations for algorithms
│   │   ├── aoi.py         # Area of Interest utilities
│   │   └── manager.py     # Job management utilities
│   ├── templates/         # Shared HTML templates
│   ├── static/            # CSS, JavaScript, images
│   └── requirements.txt   # Python dependencies
├── config/                # Docker and deployment configurations
│   ├── db/Dockerfile      # PostgreSQL with PostGIS setup
│   └── nginx/             # Nginx reverse proxy configuration
├── docker-compose.yml     # Container orchestration
└── scripts/               # Utility scripts
```

### Key Components

- **Models**: PostGIS-enabled models for spatial data (countries, regions, jobs)
- **Views**: AJAX-heavy views for real-time algorithm interaction
- **Templates**: Bootstrap 5-based responsive templates
- **Static Files**: Material Design components and custom JavaScript
- **Algorithms**: Integration with Trends.Earth processing algorithms
- **Job Management**: Asynchronous task processing and result storage

### External Dependencies

- **[Trends.Earth API](https://api.trends.earth)**: Backend processing services
- **[Google Earth Engine](https://earthengine.google.com/)**: Satellite data processing
- **[trends.earth-schemas](https://github.com/ConservationInternational/trends.earth-schemas)**: Data schema definitions
- **PostGIS**: Spatial database operations and geometric processing

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Database Configuration
POSTGRES_DB=te_web
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# API Configuration
API_URL=https://api.trends.earth
API_TOKEN=your-api-token

# Rollbar Configuration (Optional)
ROLLBAR_TOKEN=your_rollbar_token_here
ROLLBAR_ENVIRONMENT=development
```

### Algorithm Configuration

Algorithm definitions are stored in `app/utils/data/scripts.json` and can be customized for different processing workflows.

## Exception Logging

The application includes comprehensive exception logging through Rollbar integration:

```python
from utils.logger import log, log_exception
from utils.rollbar_config import report_message, report_exception

# Automatic exception capture for all uncaught exceptions
# Manual logging with different levels
log("Info message", 0)      # INFO level
log("Warning message", 1)   # WARNING level 
log("Error message", 2)     # ERROR level

# Exception logging with context
try:
    # code that might fail
    pass
except Exception:
    log_exception(sys.exc_info(), {"context": "additional_data"})
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Run tests: `cd app && python test_simple.py`
4. Check code quality: `ruff check app/ && ruff format --check app/`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a Pull Request

## Related Projects

- **[trends.earth](https://github.com/ConservationInternational/trends.earth)**: QGIS plugin and core algorithms
- **[trends.earth-API](https://github.com/ConservationInternational/trends.earth-api)**: Backend API services
- **[trends.earth-schemas](https://github.com/ConservationInternational/trends.earth-schemas)**: Data schema definitions

## License

This project is part of the Trends.Earth ecosystem developed by Conservation International, NASA, and Lund University.

## Support

- **Documentation**: [trends.earth/docs](https://trends.earth/docs/en)
- **Issues**: [GitHub Issues](https://github.com/ConservationInternational/trendsearth-web/issues)
- **Website**: [trends.earth](https://trends.earth)
