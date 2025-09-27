"""
Marshmallow schema for SDG 15.3.1 sub-indicators job parameters.
"""

from marshmallow import fields, validate, validates_schema, ValidationError
from .base import BaseJobSchema, DateRangeSchema
import json


class SubIndicatorsSchema(BaseJobSchema, DateRangeSchema):
    """Schema for SDG 15.3.1 sub-indicators script parameters."""
    
    # Rename date fields to match expected parameter names  
    initial_year_de = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))
    target_year_de = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))
    
    # Land cover transition matrix data
    tdata = fields.Str(required=True, validate=validate.Length(min=1))
    
    # Sub-indicator selection
    calculate_productivity = fields.Bool(
        load_default=True,
        metadata={'title': 'Calculate productivity', 'description': 'Include land productivity sub-indicator'}
    )
    
    calculate_land_cover = fields.Bool(
        load_default=True, 
        metadata={'title': 'Calculate land cover', 'description': 'Include land cover change sub-indicator'}
    )
    
    calculate_soil_carbon = fields.Bool(
        load_default=True,
        metadata={'title': 'Calculate soil carbon', 'description': 'Include soil organic carbon sub-indicator'}
    )
    
    # Productivity parameters (when enabled)
    ndvi_dataset = fields.Str(validate=validate.Length(min=1))
    prod_mode = fields.Str(validate=validate.OneOf(['trajectory', 'performance', 'state']))
    
    # Population data is automatically included for affected population calculations
    # Uses "users/geflanddegradation/toolbox_datasets/worldpop_mf_v1_300m"

    @validates_schema
    def validate_transition_data(self, data, **kwargs):
        """Validate that tdata contains valid transition matrix JSON."""
        try:
            tdata = json.loads(data['tdata'])
            if not isinstance(tdata, (list, dict)):
                raise ValidationError('tdata must be valid JSON array or object')
        except (json.JSONDecodeError, TypeError):
            raise ValidationError('tdata must be valid JSON')
    
    @validates_schema
    def validate_sub_indicator_selection(self, data, **kwargs):
        """Validate that at least one sub-indicator is selected."""
        indicators = [
            data.get('calculate_productivity', True),
            data.get('calculate_land_cover', True), 
            data.get('calculate_soil_carbon', True)
        ]
        if not any(indicators):
            raise ValidationError('At least one sub-indicator must be selected')

    class Meta:
        script_name = "sdg-15-3-1-sub-indicators"
        description = "SDG 15.3.1 sub-indicators analysis parameters"