# Marshmallow Schemas for Trends.Earth Job Parameters

This directory contains marshmallow schemas for validating input parameters to all supported Trends.Earth Google Earth Engine (GEE) scripts. The schemas provide comprehensive validation, avoid code duplication through shared base schemas, and **reuse existing `te_schemas` wherever relevant and possible** to maintain consistency with the existing codebase.

## Overview

The schema implementation includes:

- **Base schemas** for common parameters shared across scripts, reusing `te_schemas.jobs.Job` fields
- **Script-specific schemas** for each of the 9 supported GEE scripts with `te_schemas` integration  
- **Schema registry** for dynamic schema retrieval by script name
- **Utility functions** for integration with existing job processing
- **Comprehensive validation** with descriptive error messages and `te_schemas` compatibility
- **Metadata support** for future GUI generation

## te_schemas Integration

This implementation **reuses existing `te_schemas`** wherever relevant and possible:

### Required Dependencies

- **`te_schemas`**: Required dependency providing land cover, productivity, job, and AOI schemas
- **GDAL**: Required for geospatial operations and te_schemas.aoi functionality
- Both dependencies are mandatory for proper operation

### Reused te_schemas Components

1. **`te_schemas.jobs.Job`** - Base job fields (`task_name`, `task_notes`) are reused in `BaseJobSchema`
2. **`te_schemas.aoi.AOI`** - Used for AOI geometry validation and processing
3. **`te_schemas.land_cover.LCTransitionDefinitionDeg`** - Used for land cover matrix validation in:
   - `LandCoverSchema`
   - `SubIndicatorsSchema`
4. **`te_schemas.productivity.ProductivityMode`** - Used for productivity mode validation in:
   - `ProductivitySchema` 
   - `SubIndicatorsSchema`

## Schema Structure

### Base Schemas (`schemas/base.py`)

- **`BaseJobSchema`**: Common parameters with `te_schemas.jobs.Job` field reuse
- **`AOISchema`**: Area of Interest parameters using `te_schemas.aoi.AOI`
- **`TaskInfoSchema`**: Task metadata using `te_schemas.jobs.Job` fields
- **`DateRangeSchema`**: Year range validation with cross-field checks

### Script-Specific Schemas with te_schemas Integration

1. **`LandCoverSchema`** (`schemas/land_cover.py`)
   - **te_schemas integration**: Uses `LCTransitionDefinitionDeg` for matrix validation
   - Land cover change parameters with robust transition matrix validation
   - Date range: initial_year_de, target_year_de

2. **`ProductivitySchema`** (`schemas/productivity.py`)
   - **te_schemas integration**: Uses `ProductivityMode` enum for mode validation
   - Land productivity analysis parameters with proper mode handling
   - Supports both numeric (1,2,3) and string mode inputs
   - NDVI dataset selection and trajectory method validation

3. **`SubIndicatorsSchema`** (`schemas/sub_indicators.py`)
   - **te_schemas integration**: Uses both `LCTransitionDefinitionDeg` and `ProductivityMode`
   - SDG 15.3.1 sub-indicators analysis with comprehensive validation
   - Multiple sub-indicator selection with cross-validation

4. **Other Schemas** (`drought.py`, `urban_change.py`, etc.)
   - Maintain consistency with existing parameter patterns
   - Ready for future `te_schemas` integration as more modules become available

## Usage

### Basic Schema Validation with te_schemas

```python
from job.schemas import schema_registry

# Land cover validation using te_schemas.land_cover.LCTransitionDefinitionDeg
try:
    validated_data = schema_registry.validate_parameters('land-cover', {
        'aoi_id': 1,
        'task_name': 'Land Cover Analysis',
        'initial_year_de': 2001,
        'target_year_de': 2020,
        'tdata': '{"0": {"0": "0", "1": "-"}, "1": {"0": "+", "1": "0"}}'
    })
    print("Matrix validated using te_schemas!")
except ValidationError as e:
    print(f"Validation failed: {e.messages}")

# Productivity validation using te_schemas.productivity.ProductivityMode
validated_data = schema_registry.validate_parameters('productivity', {
    'aoi_id': 1,
    'task_name': 'Productivity Analysis',
    'year_initial': 2001,
    'year_final': 2020,
    'ndvi_dataset': 'MODIS',
    'prod_mode': 1  # Automatically converted to ProductivityMode.TRENDS_EARTH_5_CLASS_LPD
})
```

3. **`DroughtVulnerabilitySchema`** (`schemas/drought.py`)
   - Drought vulnerability analysis
   - SPI lag parameter (1-12 months)
   - Predefined datasets (WorldPop, GPCC)

4. **`UrbanChangeSchema`** (`schemas/urban_change.py`)
   - Urban area change analysis
   - 7 threshold parameters with range validation
   - Cross-field validation (urban > suburban percentage)

5. **`UNCCDReportingSchema`** (`schemas/unccd.py`)
   - UNCCD reporting data generation
   - Date range and SPI lag parameters

6. **`RestorationBiomassSchema`** (`schemas/restoration.py`)
   - Biomass restoration analysis
   - Biomass data source selection

7. **`SoilCarbonSchema`** (`schemas/soil_carbon.py`)
   - Soil organic carbon change analysis
   - Calculation method and climate regime parameters

8. **`TotalCarbonSchema`** (`schemas/total_carbon.py`)
   - Total carbon change analysis
   - Carbon pool selection options

9. **`SubIndicatorsSchema`** (`schemas/sub_indicators.py`)
   - SDG 15.3.1 sub-indicators analysis
   - Multiple sub-indicator selection
   - Complex parameter combinations

## Usage

### Basic Schema Validation

```python
from job.schemas import schema_registry

# Validate parameters for a specific script
try:
    validated_data = schema_registry.validate_parameters('land-cover', {
        'aoi_id': 1,
        'task_name': 'Land Cover Analysis',
        'initial_year_de': 2001,
        'target_year_de': 2020,
        'tdata': '{"transition": "matrix"}'
    })
    print("Validation successful!")
except ValidationError as e:
    print(f"Validation failed: {e.messages}")
```

### Dynamic Schema Information

```python
# Get all available schemas
schemas = schema_registry.list_available_schemas()
print(f"Available schemas: {schemas}")

# Get schema description
description = schema_registry.get_schema_description('productivity')
print(f"Description: {description}")

# Get field definitions for GUI generation
fields = schema_registry.get_schema_fields('urban-area')
for field_name, field_info in fields.items():
    print(f"{field_name}: {field_info['type']} ({'required' if field_info['required'] else 'optional'})")
```

### Integration with Job Processing

```python
from job.schema_utils import validate_and_transform_parameters

# Complete validation and transformation
try:
    payloads = validate_and_transform_parameters('drought-vulnerability', request)
    # payloads is ready for API submission
except ValidationError as e:
    return JsonResponse({'error': e.messages}, status=400)
```

## Testing

The schemas include comprehensive tests covering:

- **Basic validation** for all schema types
- **Edge cases** and boundary values  
- **Error handling** for invalid inputs
- **Schema metadata** extraction
- **Field structure** validation

Run tests:
```bash
cd app/job
python test_schemas.py           # Basic functionality tests
python test_comprehensive_schemas.py  # Comprehensive validation tests
```

## Future GUI Generation

The schemas are designed to support dynamic GUI generation:

```python
from job.schema_utils import get_schema_fields_for_gui

# Get GUI-formatted field definitions
gui_fields = get_schema_fields_for_gui('productivity')

# Each field includes:
# - name, type, required status
# - label and description for display
# - validation constraints (min/max, options, etc.)
# - default values
```

## Error Handling

Schemas provide detailed validation errors:

```python
try:
    schema_registry.validate_parameters('land-cover', invalid_params)
except ValidationError as e:
    # e.messages contains detailed field-level errors
    # Example: {'aoi_id': ['Must be greater than or equal to 1']}
```

## Extension

To add a new script schema:

1. Create a new schema file in `schemas/`
2. Inherit from `BaseJobSchema` and add script-specific fields
3. Add validation methods as needed
4. Register the schema in `schemas/registry.py`
5. Add tests for the new schema

## Dependencies

- `marshmallow>=4.0`: Core schema functionality
- `marshmallow-dataclass`: For @dataclass support (used in base schemas)

The schemas are independent of Django models and can be used for validation without a full Django setup.