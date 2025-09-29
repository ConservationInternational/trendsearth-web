"""
Marshmallow schema for UNCCD reporting job parameters.
"""

from marshmallow import fields, validate
from .base import BaseJobSchema, DateRangeSchema


class UNCCDReportingSchema(BaseJobSchema, DateRangeSchema):
    """Schema for UNCCD reporting script parameters."""

    # Rename date fields to match expected parameter names
    initial_year_de = fields.Int(
        required=True, validate=validate.Range(min=1900, max=2100)
    )
    target_year_de = fields.Int(
        required=True, validate=validate.Range(min=1900, max=2100)
    )

    # SPI lag parameter for drought analysis
    lag_cb = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=12),
        metadata={
            "title": "SPI lag (months)",
            "description": "Number of months for SPI calculation lag",
        },
    )

    # UNCCD reporting uses predefined datasets:
    # Population: "Gridded Population Count" from WorldPop
    # SPI: "GPCC V6 (Global Precipitation Climatology Centre)"

    class Meta:
        script_name = "unccd-report"
        description = "UNCCD reporting data generation parameters"
