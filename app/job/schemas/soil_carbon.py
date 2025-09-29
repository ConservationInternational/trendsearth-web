"""
Marshmallow schema for soil organic carbon job parameters.
"""

from marshmallow import fields, validate
from .base import BaseJobSchema, DateRangeSchema


class SoilCarbonSchema(BaseJobSchema, DateRangeSchema):
    """Schema for soil organic carbon change script parameters."""

    # Rename date fields to match expected parameter names
    initial_year_de = fields.Int(
        required=True, validate=validate.Range(min=1900, max=2100)
    )
    target_year_de = fields.Int(
        required=True, validate=validate.Range(min=1900, max=2100)
    )

    # SOC calculation method
    soc_method = fields.Str(
        validate=validate.OneOf(["stock-change", "emissions-factor"]),
        load_default="stock-change",
        metadata={
            "title": "SOC calculation method",
            "description": "Method for calculating soil organic carbon change",
        },
    )

    # Climate regime for SOC calculations
    climate_regime = fields.Str(
        validate=validate.OneOf(
            ["temperate-dry", "temperate-moist", "tropical-dry", "tropical-moist"]
        ),
        metadata={
            "title": "Climate regime",
            "description": "Climate regime for SOC calculations",
        },
    )

    class Meta:
        script_name = "soil-organic-carbon"
        description = "Soil organic carbon change analysis parameters"
