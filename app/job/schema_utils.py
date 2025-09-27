"""
Utility functions for integrating marshmallow schemas with job processing.

These utilities provide helpers for validating parameters, populating AOI data,
and transforming validated data into the format expected by the GEE scripts.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from marshmallow import ValidationError

from account import models as accountmodels
from .schemas import schema_registry

logger = logging.getLogger(__name__)

# Default CRS used across all scripts
DEFAULT_CRS = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'


def validate_job_parameters(script_name: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate job parameters using the appropriate schema for the script.
    
    Args:
        script_name: Name of the script (e.g., 'land-cover', 'productivity')
        request_data: Raw request data from POST parameters
        
    Returns:
        Validated and processed parameters
        
    Raises:
        ValidationError: If validation fails
        ValueError: If no schema found for the script
    """
    try:
        # Get the schema for this script
        schema = schema_registry.get_schema_instance(script_name)
        if not schema:
            raise ValueError(f"No schema found for script: {script_name}")
        
        # Validate the input parameters
        validated_data = schema.load(request_data)
        
        # Populate AOI data if aoi_id is provided
        if 'aoi_id' in validated_data:
            validated_data = populate_aoi_data(validated_data)
        
        logger.info(f"Successfully validated parameters for {script_name}")
        return validated_data
        
    except ValidationError as e:
        logger.error(f"Validation failed for {script_name}: {e.messages}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error validating {script_name}: {e}")
        raise


def populate_aoi_data(validated_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Populate AOI geometry data from the database using aoi_id.
    
    Args:
        validated_data: Validated parameters containing aoi_id
        
    Returns:
        Parameters with populated geojsons, crs, and crosses_180th fields
    """
    try:
        aoi_id = validated_data.get('aoi_id')
        if not aoi_id:
            return validated_data
        
        # Fetch AOI from database
        aoi = accountmodels.Aoi.objects.get(id=aoi_id)
        
        # Populate geometry fields
        validated_data['geojsons'] = json.dumps([json.loads(aoi.geom.json)])
        validated_data['crs'] = DEFAULT_CRS
        validated_data['crosses_180th'] = False  # Could be calculated if needed
        
        logger.debug(f"Populated AOI data for aoi_id: {aoi_id}")
        return validated_data
        
    except accountmodels.Aoi.DoesNotExist:
        raise ValidationError(f"AOI with id {aoi_id} not found")
    except Exception as e:
        logger.error(f"Error populating AOI data: {e}")
        raise


def get_schema_for_script(script_name: str) -> Optional[Any]:
    """
    Get the marshmallow schema instance for a script.
    
    Args:
        script_name: Name of the script
        
    Returns:
        Schema instance or None if not found
    """
    return schema_registry.get_schema_instance(script_name)


def get_schema_fields_for_gui(script_name: str) -> Optional[Dict[str, Any]]:
    """
    Get schema field definitions formatted for dynamic GUI generation.
    
    Args:
        script_name: Name of the script
        
    Returns:
        Dictionary of field definitions with metadata for GUI generation
    """
    fields = schema_registry.get_schema_fields(script_name)
    if not fields:
        return None
    
    # Format fields for GUI generation
    gui_fields = {}
    for field_name, field_info in fields.items():
        # Skip dump_only fields (not for input)
        if field_info.get('dump_only'):
            continue
            
        gui_field = {
            'name': field_name,
            'type': _map_field_type_to_gui(field_info['type']),
            'required': field_info['required'],
            'label': field_info['metadata'].get('title', field_name.replace('_', ' ').title()),
            'description': field_info['metadata'].get('description', ''),
            'default': field_info.get('load_default'),
        }
        
        # Add validation constraints
        if 'validators' in field_info:
            gui_field['validation'] = _extract_validation_constraints(field_info['validators'])
        
        gui_fields[field_name] = gui_field
    
    return gui_fields


def _map_field_type_to_gui(field_type: str) -> str:
    """Map marshmallow field types to GUI form field types."""
    type_mapping = {
        'String': 'text',
        'Int': 'number',
        'Float': 'number',
        'Bool': 'checkbox',
        'Raw': 'textarea',  # For JSON data
    }
    return type_mapping.get(field_type, 'text')


def _extract_validation_constraints(validators: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract validation constraints for GUI field validation."""
    constraints = {}
    
    for validator in validators:
        validator_type = validator.get('type')
        validator_args = validator.get('args', {})
        
        if validator_type == 'Range':
            if 'min' in validator_args:
                constraints['min'] = validator_args['min']
            if 'max' in validator_args:
                constraints['max'] = validator_args['max']
        elif validator_type == 'Length':
            if 'min' in validator_args:
                constraints['minLength'] = validator_args['min']
            if 'max' in validator_args:
                constraints['maxLength'] = validator_args['max']
        elif validator_type == 'OneOf':
            constraints['options'] = validator_args.get('choices', [])
    
    return constraints


def list_available_schemas() -> List[str]:
    """
    Get a list of all available schema names.
    
    Returns:
        List of script names that have schemas
    """
    return schema_registry.list_available_schemas()


def get_schema_description(script_name: str) -> Optional[str]:
    """
    Get the description for a schema.
    
    Args:
        script_name: Name of the script
        
    Returns:
        Schema description or None if not found
    """
    return schema_registry.get_schema_description(script_name)


def validate_and_transform_parameters(script_name: str, request) -> List[Dict[str, Any]]:
    """
    Complete parameter validation and transformation for job processing.
    
    This function validates parameters using the schema and transforms them
    into the format expected by the existing job processing functions.
    
    Args:
        script_name: Name of the script
        request: Django request object with POST data
        
    Returns:
        List of payload dictionaries ready for API submission
        
    Raises:
        ValidationError: If validation fails
    """
    # Convert request.POST to dictionary
    request_data = dict(request.POST.items())
    
    # Special handling for list/array fields if needed
    # (e.g., if frontend sends multiple values for same parameter)
    for key, value in request.POST.lists():
        if len(value) > 1:  # Multiple values for same key
            request_data[key] = value
    
    # Validate parameters
    validated_data = validate_job_parameters(script_name, request_data)
    
    # For now, return as single payload in list (some scripts may return multiple)
    # Future enhancement: detect when multiple payloads needed (e.g., multiple periods)
    return [validated_data]