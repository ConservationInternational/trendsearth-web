"""
Schema registry for dynamic retrieval of marshmallow schemas by script name.
"""

from typing import Dict, Type, Optional, Any
from marshmallow import Schema
import logging

logger = logging.getLogger(__name__)


class SchemaRegistry:
    """
    Registry for dynamically retrieving and using marshmallow schemas
    for different Trends.Earth GEE scripts.
    """

    def __init__(self):
        self._schemas: Dict[str, Type[Schema]] = {}
        self._register_default_schemas()

    def _register_default_schemas(self):
        """Register all default schemas on initialization."""
        try:
            from .land_cover import LandCoverSchema
            from .productivity import ProductivitySchema
            from .drought import DroughtVulnerabilitySchema
            from .urban_change import UrbanChangeSchema
            from .unccd import UNCCDReportingSchema
            from .restoration import RestorationBiomassSchema
            from .soil_carbon import SoilCarbonSchema
            from .total_carbon import TotalCarbonSchema
            from .sub_indicators import SubIndicatorsSchema

            # Register schemas by their script names
            self.register("land-cover", LandCoverSchema)
            self.register("productivity", ProductivitySchema)
            self.register("drought-vulnerability", DroughtVulnerabilitySchema)
            self.register("urban-area", UrbanChangeSchema)
            self.register("unccd-report", UNCCDReportingSchema)
            self.register("restoration-biomass", RestorationBiomassSchema)
            self.register("soil-organic-carbon", SoilCarbonSchema)
            self.register("total-carbon", TotalCarbonSchema)
            self.register("sdg-15-3-1-sub-indicators", SubIndicatorsSchema)

            logger.info(f"Registered {len(self._schemas)} schemas")

        except ImportError as e:
            logger.error(f"Failed to import schemas: {e}")

    def register(self, script_name: str, schema_class: Type[Schema]):
        """
        Register a schema class for a script name.

        Args:
            script_name: The name of the script (e.g., 'land-cover')
            schema_class: The marshmallow schema class
        """
        self._schemas[script_name] = schema_class
        logger.debug(f"Registered schema for script: {script_name}")

    def get_schema(self, script_name: str) -> Optional[Type[Schema]]:
        """
        Get a schema class by script name.

        Args:
            script_name: The name of the script

        Returns:
            The schema class or None if not found
        """
        return self._schemas.get(script_name)

    def get_schema_instance(self, script_name: str) -> Optional[Schema]:
        """
        Get an instantiated schema by script name.

        Args:
            script_name: The name of the script

        Returns:
            An instance of the schema or None if not found
        """
        schema_class = self.get_schema(script_name)
        if schema_class:
            return schema_class()
        return None

    def validate_parameters(
        self, script_name: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate parameters for a specific script using its schema.

        Args:
            script_name: The name of the script
            parameters: Dictionary of parameters to validate

        Returns:
            Validated and processed parameters

        Raises:
            ValidationError: If validation fails
            ValueError: If schema not found for script
        """
        schema = self.get_schema_instance(script_name)
        if not schema:
            raise ValueError(f"No schema registered for script: {script_name}")

        # Validate and return the processed data
        validated_data = schema.load(parameters)
        logger.debug(f"Successfully validated parameters for {script_name}")
        return validated_data

    def get_schema_fields(self, script_name: str) -> Optional[Dict[str, Any]]:
        """
        Get field definitions for a schema to support dynamic GUI generation.

        Args:
            script_name: The name of the script

        Returns:
            Dictionary of field definitions with metadata, or None if schema not found
        """
        schema = self.get_schema_instance(script_name)
        if not schema:
            return None

        fields_info = {}
        for field_name, field_obj in schema.fields.items():
            field_info = {
                "type": type(field_obj).__name__,
                "required": field_obj.required,
                "allow_none": field_obj.allow_none,
                "missing": getattr(field_obj, "missing", None),
                "default": getattr(field_obj, "default", None),
                "metadata": field_obj.metadata,
            }

            # Add validation info if available
            if hasattr(field_obj, "validators"):
                field_info["validators"] = [
                    {
                        "type": type(validator).__name__,
                        "args": getattr(validator, "__dict__", {}),
                    }
                    for validator in field_obj.validators
                ]

            fields_info[field_name] = field_info

        return fields_info

    def list_available_schemas(self) -> list[str]:
        """
        Get a list of all registered schema names.

        Returns:
            List of script names that have registered schemas
        """
        return list(self._schemas.keys())

    def get_schema_description(self, script_name: str) -> Optional[str]:
        """
        Get the description for a schema.

        Args:
            script_name: The name of the script

        Returns:
            Schema description or None if not found
        """
        schema_class = self.get_schema(script_name)
        if schema_class and hasattr(schema_class, "Meta"):
            return getattr(schema_class.Meta, "description", None)
        return None
