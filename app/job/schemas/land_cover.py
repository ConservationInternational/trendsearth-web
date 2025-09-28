"""
Marshmallow schema for land cover change job parameters.

This schema reuses te_schemas.land_cover.LCTransitionDefinitionDeg for 
transition matrix validation to maintain consistency with existing code.
te_schemas and GDAL are required dependencies for this code to work.
"""

from marshmallow import fields, validate, validates_schema, ValidationError, post_load
from .base import BaseJobSchema
import json

from te_schemas.land_cover import LCTransitionDefinitionDeg
from utils.util import table_to_matrix


class LandCoverSchema(BaseJobSchema):
    """Schema for land cover change script parameters using te_schemas validation."""
    
    # Date fields specific to land cover (different naming from base DateRangeSchema)
    initial_year_de = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))
    target_year_de = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))
    
    # Land cover transition matrix data (from frontend table)
    tdata = fields.Str(required=True, validate=validate.Length(min=1))
    
    # Legend nesting configuration (populated during processing)
    legend_nesting = fields.Raw(dump_only=True)
    trans_matrix = fields.Raw(dump_only=True)

    @validates_schema
    def validate_date_range(self, data, **kwargs):
        """Validate that target year is after initial year."""
        if data['target_year_de'] <= data['initial_year_de']:
            raise ValidationError('target_year_de must be greater than initial_year_de')

    @validates_schema
    def validate_transition_data(self, data, **kwargs):
        """Validate transition matrix using te_schemas.land_cover.LCTransitionDefinitionDeg."""
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

    @post_load
    def process_transition_matrix(self, data, **kwargs):
        """Post-process the validated transition matrix."""
        if '_validated_matrix' in data:
            # Serialize the validated matrix for API submission
            data['trans_matrix'] = LCTransitionDefinitionDeg.Schema().dump(data['_validated_matrix'])
            # Remove the temporary field
            del data['_validated_matrix']
        return data

    class Meta:
        script_name = "land-cover"
        description = "Land cover change analysis parameters using te_schemas validation"