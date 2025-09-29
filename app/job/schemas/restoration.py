"""
Marshmallow schema for restoration biomass job parameters.
"""

from marshmallow import fields, validate
from .base import BaseJobSchema, DateRangeSchema


class RestorationBiomassSchema(BaseJobSchema, DateRangeSchema):
    """Schema for restoration biomass script parameters."""

    # Biomass data source selection
    biomass_data = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        metadata={
            "title": "Biomass data source",
            "description": "Source dataset for biomass calculations",
        },
    )

    # The script calculates potential change in biomass with restoration
    # using the selected biomass dataset

    class Meta:
        script_name = "restoration-biomass"
        description = "Restoration biomass change analysis parameters"
