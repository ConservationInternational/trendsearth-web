"""
Marshmallow schemas for validating job parameters for Trends.Earth GEE scripts.

This module provides schema definitions for all supported Trends.Earth scripts,
with shared base schemas for common parameters to avoid code duplication.
"""

from .base import BaseJobSchema, AOISchema, TaskInfoSchema, DateRangeSchema
from .land_cover import LandCoverSchema
from .productivity import ProductivitySchema
from .drought import DroughtVulnerabilitySchema
from .urban_change import UrbanChangeSchema
from .unccd import UNCCDReportingSchema
from .restoration import RestorationBiomassSchema
from .soil_carbon import SoilCarbonSchema
from .total_carbon import TotalCarbonSchema
from .sub_indicators import SubIndicatorsSchema
from .registry import SchemaRegistry

# Main schema registry for dynamic schema retrieval
schema_registry = SchemaRegistry()

__all__ = [
    "BaseJobSchema",
    "AOISchema",
    "TaskInfoSchema",
    "DateRangeSchema",
    "LandCoverSchema",
    "ProductivitySchema",
    "DroughtVulnerabilitySchema",
    "UrbanChangeSchema",
    "UNCCDReportingSchema",
    "RestorationBiomassSchema",
    "SoilCarbonSchema",
    "TotalCarbonSchema",
    "SubIndicatorsSchema",
    "SchemaRegistry",
    "schema_registry",
]
