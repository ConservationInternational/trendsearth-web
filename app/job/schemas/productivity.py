"""
Marshmallow schema for land productivity job parameters.
"""

from marshmallow import fields, validate, validates_schema, ValidationError
from .base import BaseJobSchema, DateRangeSchema


class ProductivitySchema(BaseJobSchema, DateRangeSchema):
    """Schema for land productivity script parameters."""
    
    # NDVI dataset selection
    ndvi_dataset = fields.Str(required=True, validate=validate.Length(min=1))
    
    # Productivity mode selection
    prod_mode = fields.Str(
        required=True,
        validate=validate.OneOf(['state', 'performance', 'trajectory', 'all'])
    )
    
    # Trajectory-specific parameters
    trajectory_indicator = fields.Str(validate=validate.Length(min=1))
    traj_climate = fields.Str(allow_none=True)  # Can be "null" or dataset name
    
    # Performance parameters  
    performance_n_years = fields.Int(validate=validate.Range(min=1, max=20))
    
    # State parameters
    state_use_cru_ndvi = fields.Bool(load_default=False)
    
    # Custom productivity dataset options
    custom_productivity_baseline = fields.Str(allow_none=True)
    custom_productivity_trajectory = fields.Str(allow_none=True)
    custom_productivity_performance = fields.Str(allow_none=True)
    custom_productivity_state = fields.Str(allow_none=True)

    @validates_schema
    def validate_trajectory_params(self, data, **kwargs):
        """Validate trajectory-specific parameters when trajectory mode is selected."""
        prod_mode = data.get('prod_mode')
        
        if prod_mode in ['trajectory', 'all']:
            if not data.get('trajectory_indicator'):
                raise ValidationError('trajectory_indicator is required for trajectory mode')
        
        # If trajectory_indicator is set, validate it's a known indicator
        trajectory_indicator = data.get('trajectory_indicator')
        if trajectory_indicator:
            valid_indicators = [
                'NDVI trends',
                'Pixel RESTREND', 
                'Rain Use Efficiency (RUE)',
                'Water Use Efficiency (WUE)'
            ]
            if trajectory_indicator not in valid_indicators:
                raise ValidationError(f'trajectory_indicator must be one of: {valid_indicators}')

    @validates_schema 
    def validate_performance_params(self, data, **kwargs):
        """Validate performance-specific parameters when performance mode is selected."""
        prod_mode = data.get('prod_mode')
        
        if prod_mode in ['performance', 'all']:
            if not data.get('performance_n_years'):
                data['performance_n_years'] = 5  # Default value

    class Meta:
        script_name = "productivity"
        description = "Land productivity analysis parameters"