"""
Marshmallow schema for drought vulnerability job parameters.
"""

from marshmallow import fields, validate
from .base import BaseJobSchema, DateRangeSchema


class DroughtVulnerabilitySchema(BaseJobSchema, DateRangeSchema):
    """Schema for drought vulnerability script parameters."""
    
    # SPI (Standardized Precipitation Index) lag parameter
    lag_cb = fields.Int(
        required=True, 
        validate=validate.Range(min=1, max=12),
        metadata={'title': 'SPI lag (months)', 'description': 'Number of months for SPI calculation lag'}
    )
    
    # Drought vulnerability datasets are predefined in the backend
    # Population dataset: "Gridded Population Count" from WorldPop
    # SPI dataset: "GPCC V6 (Global Precipitation Climatology Centre)"
    # Land cover dataset: "users/geflanddegradation/toolbox_datasets/lcov_esacc_1992_2022"

    class Meta:
        script_name = "drought-vulnerability"
        description = "Drought vulnerability analysis parameters"