"""
Marshmallow schema for total carbon change job parameters.
"""

from marshmallow import fields, validate
from .base import BaseJobSchema, DateRangeSchema


class TotalCarbonSchema(BaseJobSchema, DateRangeSchema):
    """Schema for total carbon change script parameters."""
    
    # Carbon pool selections
    include_soil_carbon = fields.Bool(
        load_default=True,
        metadata={'title': 'Include soil carbon', 'description': 'Include soil organic carbon in calculations'}
    )
    
    include_biomass_carbon = fields.Bool(
        load_default=True,
        metadata={'title': 'Include biomass carbon', 'description': 'Include above and below ground biomass carbon'}
    )
    
    # Biomass data source for carbon calculations
    biomass_data = fields.Str(
        validate=validate.Length(min=1),
        metadata={'title': 'Biomass data source', 'description': 'Source dataset for biomass carbon calculations'}
    )

    class Meta:
        script_name = "total-carbon"
        description = "Total carbon change analysis parameters"