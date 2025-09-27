# Trends.Earth Web - Copilot Instructions

## Repository Overview

The **trendsearth-web** repository is a Django-based web application that serves as the frontend interface for Trends.Earth, a platform for monitoring land degradation and environmental indicators. This application provides a user-friendly web interface for running Earth observation algorithms, viewing results, and managing user data related to land degradation monitoring.

### High-Level Repository Information

- **Repository Size**: ~8,754 lines of Python code, 285 frontend files (HTML/CSS/JS)
- **Project Type**: Django web application with geospatial capabilities
- **Primary Languages**: Python (Django), JavaScript, HTML/CSS
- **Framework**: Django 4.2, PostgreSQL with PostGIS
- **Runtime**: Python 3.13
- **Frontend**: Bootstrap 5 (Material Design), vanilla JavaScript
- **Dependencies**: GDAL/OGR for geospatial operations, PostGIS for spatial database

## Build Instructions

### GitHub Copilot Environment Setup

**IMPORTANT**: When working in GitHub Copilot's environment, all dependencies are pre-installed via `.github/copilot-setup-steps.yml`. The following are already available:

✅ **Pre-installed Dependencies:**
- **Python 3.13** - Ready for Django development
- **GDAL libraries** - System-wide GDAL/OGR with Python bindings installed
- **PostgreSQL client tools** - For database connections (PostGIS extensions available)
- **te_schemas** - Trends.Earth schemas package (from GitHub master branch)
- **te_algorithms** - Trends.Earth algorithms package (from GitHub master branch)
- **Testing tools** - ruff for code quality checks
- **All Python requirements** - Django 4.2+ and all app dependencies from `requirements.txt`

✅ **Ecosystem Repositories Available for Reference:**
- `trends.earth` - QGIS plugin and Google Earth Engine scripts (in `/tmp/trends.earth/`)
- `trends.earth-api` - Backend API services (in `/tmp/trends.earth-api/`)
- `trends.earth-api-ui` - Alternative API interface (in `/tmp/trends.earth-api-ui/`)

**In Copilot environment, you can immediately:**
- Start development without dependency installation
- Run tests: `cd app/ && python test_simple.py`
- Check code quality: `ruff check app/ && ruff format --check app/`
- Reference related repositories in `/tmp/` for cross-ecosystem development

### Manual Prerequisites (for local development outside Copilot)

**Only install these if working outside GitHub Copilot environment:**

1. **Python 3.13** - Required for Django compatibility
2. **GDAL libraries** - Critical for geospatial operations (will cause Django startup failures if missing)
3. **PostgreSQL with PostGIS extension** - Required for spatial database operations
4. **Docker and Docker Compose** - For containerized development (recommended)

### Environment Setup

**In GitHub Copilot Environment:**
All dependencies are pre-installed. You can immediately start development and testing:

```bash
# Verify everything is ready (should pass immediately)
cd app/
python test_simple.py

# Check code quality (tools pre-installed)
ruff check app/ && ruff format --check app/
```

**For Manual Setup (outside Copilot):**

1. **Dependencies Installation** (takes ~60 seconds):
   ```bash
   cd app/
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Install Code Quality Tools**:
   ```bash
   pip install ruff
   ```

### Build Commands

**Important**: The application has two primary build approaches:

#### Docker-based Build (Recommended)
```bash
# Build and run with Docker Compose (takes ~3-5 minutes first time)
docker-compose up --build
```

**Note**: Docker build requires `.env` file with database credentials. The application will be available on port 9000.

#### Local Development Build
```bash
cd app/

# Run database migrations (requires running PostgreSQL with PostGIS)
python manage.py migrate

# Start development server
python manage.py runserver 0.0.0.0:9000
```

**Critical**: Local builds will fail without GDAL libraries and a running PostGIS database. Error message: `ImproperlyConfigured: Could not find the GDAL library`.

### Testing

1. **Smoke Tests** (takes ~5 seconds):
   ```bash
   cd app/
   python test_simple.py
   ```

2. **Code Quality Checks** (takes ~10 seconds):
   ```bash
   python -m ruff check app/
   python -m ruff format --check app/
   ```

**Test Results**: Smoke tests validate Python syntax (120 files) and basic Django imports. All tests must pass before making changes.

### Validation Pipeline

The repository uses GitHub Actions for CI/CD:

1. **Testing Pipeline** (`.github/workflows/testing.yml`):
   - Runs on Python 3.13
   - Executes smoke tests via `python test_simple.py`

2. **Code Quality Pipeline** (`.github/workflows/code-quality.yml`):
   - Uses ruff for code formatting and linting
   - Must pass before merge approval

**Important**: Always run these locally before committing:
```bash
cd app/ && python test_simple.py && python -m ruff check app/ && python -m ruff format --check app/
```

## Project Layout and Architecture

### Directory Structure

```
/
├── .github/workflows/          # CI/CD pipelines
├── app/                       # Main Django application
│   ├── main/                  # Django project settings
│   │   ├── settings.py        # Main configuration file
│   │   ├── urls.py           # Root URL routing
│   │   └── wsgi.py           # WSGI application entry
│   ├── account/              # User management and geographical data
│   │   ├── models.py         # Country, Region, City, User models
│   │   ├── configs/          # Geographic boundary data (JSON)
│   │   └── templates/        # User interface templates
│   ├── core/                 # Algorithm management and UI logic
│   │   ├── models.py         # Aggregation classes, user preferences
│   │   └── views.py          # AJAX endpoints for algorithms
│   ├── job/                  # Job execution and result management
│   │   ├── models.py         # Job, Status, Layer models
│   │   └── views.py          # Job execution endpoints
│   ├── utils/                # Utility functions and data
│   │   ├── conf.py           # Algorithm configurations
│   │   ├── data/             # JSON configurations for algorithms
│   │   └── aoi.py            # Area of Interest utilities
│   ├── templates/            # Shared HTML templates
│   ├── static/               # CSS, JavaScript, images
│   ├── requirements.txt      # Python dependencies
│   └── manage.py             # Django management script
├── config/                   # Docker and deployment configurations
│   ├── db/Dockerfile         # PostgreSQL with PostGIS setup
│   └── nginx/               # Nginx reverse proxy configuration
├── docker-compose.yml        # Container orchestration
└── scripts/                  # Utility scripts
```

### Key Configuration Files

- **`app/main/settings.py`**: Django settings, database configuration, API endpoints
- **`app/requirements.txt`**: Python dependencies (Django, GDAL, PostGIS drivers)
- **`docker-compose.yml`**: Container definitions for web app and database
- **`.github/workflows/`**: CI/CD pipeline definitions
- **`app/utils/data/scripts.json`**: Algorithm and script configurations

### Architectural Components

1. **Django Apps**:
   - `account`: Geographic data management (countries, regions, cities), user profiles
   - `core`: Algorithm definitions, data aggregation, UI components
   - `job`: Asynchronous job execution, result storage, layer management

2. **External Dependencies**:
   - **Trends.Earth API**: `https://api.trends.earth` (configurable via `API_URL`)
   - **Google Earth Engine**: Backend processing for satellite data
   - **PostGIS Database**: Spatial data storage and queries

3. **Key Models**:
   - `Country/Region/City`: Geographic boundaries with PostGIS geometry
   - `Script/Algorithm`: Earth observation processing definitions
   - `Job`: Asynchronous task execution tracking
   - `Layer`: Map layer management for results visualization

### Development Workflow

**In GitHub Copilot Environment (dependencies pre-installed):**

1. **Making Changes**:
   - Dependencies are ready: `te_schemas`, `te_algorithms`, Django, GDAL already installed
   - Run smoke tests: `cd app/ && python test_simple.py` (should work immediately)
   - Test with ruff: `ruff check app/ && ruff format --check app/` (tools pre-installed)

2. **Database Changes**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Adding New Features**:
   - Follow Django app structure (models → views → templates → URLs)
   - Use PostGIS for spatial operations (client tools available)
   - Follow existing AJAX patterns for frontend interactions
   - Reference ecosystem repos in `/tmp/` for compatibility checks

**For Manual Development (outside Copilot):**

1. **Making Changes**:
   - Always run smoke tests first: `cd app/ && python test_simple.py`
   - Make minimal changes to existing functionality
   - Test with ruff: `python -m ruff check app/ && python -m ruff format --check app/`

2. **Database Changes**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Adding New Features**:
   - Follow Django app structure (models → views → templates → URLs)
   - Use PostGIS for spatial operations
   - Follow existing AJAX patterns for frontend interactions

### Related Repositories

This repository is part of the Trends.Earth ecosystem. When making changes, consider compatibility with:

- **trends.earth-API**: Backend API services
- **trends.earth**: QGIS plugin and Google Earth Engine scripts  
- **trends.earth-algorithms**: Processing algorithms
- **trends.earth-schemas**: Data schema definitions
- **trends.earth-api-ui**: Alternative API interface

**In GitHub Copilot Environment:**
These related repositories are pre-cloned and available in `/tmp/` for reference:
- `/tmp/trends.earth/` - Main QGIS plugin and GEE scripts
- `/tmp/trends.earth-api/` - Backend API services  
- `/tmp/trends.earth-api-ui/` - Alternative API interface

This allows you to easily check for code duplication, understand API contracts, and ensure compatibility across the ecosystem.

**Critical**: Always check for code duplication and ensure compatibility across repositories when implementing features that might exist elsewhere in the ecosystem.

### Common Issues and Workarounds

1. **GDAL Library Errors**: Ensure GDAL is installed system-wide or use Docker environment
2. **Database Connection Failures**: Verify PostGIS is running and accessible
3. **Migration Conflicts**: Use `python manage.py showmigrations` to debug
4. **Docker Build Failures**: Clear Docker cache with `docker system prune -f`

### Trust These Instructions

These instructions have been validated against the current codebase. Only search for additional information if these instructions are incomplete or found to be incorrect. The build and test commands have been tested and verified to work correctly.