"""
Marshmallow schema for SDG 15.3.1 sub-indicators job parameters.

This schema reuses te_schemas for land cover matrix and productivity mode validation.
"""

from marshmallow import fields, validate, validates_schema, ValidationError, post_load
from .base import BaseJobSchema, DateRangeSchema
from .productivity import ProductivityModeField  # Reuse the custom field
import json

try:
    from te_schemas.land_cover import LCTransitionDefinitionDeg
    from te_schemas.productivity import ProductivityMode
    from utils.util import table_to_matrix
except ImportError:
    # Fallback if te_schemas is not available
    LCTransitionDefinitionDeg = None
    ProductivityMode = None
    table_to_matrix = None


class SubIndicatorsSchema(BaseJobSchema, DateRangeSchema):
    """Schema for SDG 15.3.1 sub-indicators script parameters using te_schemas validation."""
    
    # Date fields to match expected parameter names  
    initial_year_de = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))
    target_year_de = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))
    
    # Land cover transition matrix data (validated using te_schemas)
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
    
    # Productivity parameters (when enabled) - using te_schemas validation
    ndvi_dataset = fields.Str(validate=validate.Length(min=1))
    prod_mode = ProductivityModeField()  # Reuse the te_schemas ProductivityMode field
    
    # Processed matrix (populated during validation)
    trans_matrix = fields.Raw(dump_only=True)
    
    # Population data is automatically included for affected population calculations
    # Uses "users/geflanddegradation/toolbox_datasets/worldpop_mf_v1_300m"

    @validates_schema
    def validate_transition_data(self, data, **kwargs):
        """Validate transition matrix using te_schemas.land_cover.LCTransitionDefinitionDeg."""
        if not LCTransitionDefinitionDeg or not table_to_matrix:
            # Fallback to basic JSON validation if te_schemas not available
            try:
                tdata = json.loads(data['tdata'])
                if not isinstance(tdata, (list, dict)):
                    raise ValidationError('tdata must be valid JSON array or object')
            except (json.JSONDecodeError, TypeError):
                raise ValidationError('tdata must be valid JSON')
            return

        try:
            # Parse the table data
            form_data = json.loads(data['tdata'])
            
            # Convert to matrix format using existing utility
            matrix = table_to_matrix(form_data)
            
            # Validate using te_schemas LCTransitionDefinitionDeg
            validated_matrix = LCTransitionDefinitionDeg.Schema().load(matrix)
            
            # Store the validated matrix for later use
            data['_validated_matrix'] = validated_matrix
            
        except (json.JSONDecodeError, TypeError):
            raise ValidationError('tdata must be valid JSON')
        except Exception as e:
            raise ValidationError(f'Invalid transition matrix: {str(e)}')
    
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

    @validates_schema
    def validate_productivity_params(self, data, **kwargs):
        """Validate productivity parameters when productivity sub-indicator is enabled."""
        if data.get('calculate_productivity', True):
            if not data.get('ndvi_dataset'):
                raise ValidationError('ndvi_dataset is required when calculate_productivity is enabled')
            if not data.get('prod_mode'):
                # Set default productivity mode
                if ProductivityMode:
                    data['prod_mode'] = ProductivityMode.TRENDS_EARTH_5_CLASS_LPD
                else:
                    data['prod_mode'] = 'trajectory'

    @post_load
    def process_transition_matrix(self, data, **kwargs):
        """Post-process the validated transition matrix."""
        if LCTransitionDefinitionDeg and '_validated_matrix' in data:
            # Serialize the validated matrix for API submission
            data['trans_matrix'] = LCTransitionDefinitionDeg.Schema().dump(data['_validated_matrix'])
            # Remove the temporary field
            del data['_validated_matrix']
        return data

    class Meta:
        script_name = "sdg-15-3-1-sub-indicators"
        description = "SDG 15.3.1 sub-indicators analysis parameters using te_schemas validation"