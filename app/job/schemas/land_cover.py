"""
Marshmallow schema for land cover change job parameters.
"""

from marshmallow import fields, validate, validates_schema, ValidationError
from .base import BaseJobSchema, DateRangeSchema
import json


class LandCoverSchema(BaseJobSchema):
    """Schema for land cover change script parameters."""
    
    # Date fields specific to land cover (different naming from base DateRangeSchema)
    initial_year_de = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))
    target_year_de = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))
    
    # Land cover transition matrix data (from frontend table)
    tdata = fields.Str(required=True, validate=validate.Length(min=1))
    
    # Legend nesting configuration
    legend_nesting = fields.Raw(dump_only=True)  # Populated during processing
    trans_matrix = fields.Raw(dump_only=True)    # Populated during processing

    @validates_schema
    def validate_date_range(self, data, **kwargs):
        """Validate that target year is after initial year."""
        if data['target_year_de'] <= data['initial_year_de']:
            raise ValidationError('target_year_de must be greater than initial_year_de')

    @validates_schema
    def validate_transition_data(self, data, **kwargs):
        """Validate that tdata contains valid transition matrix JSON."""
        try:
            tdata = json.loads(data['tdata'])
            if not isinstance(tdata, (list, dict)):
                raise ValidationError('tdata must be valid JSON array or object')
        except (json.JSONDecodeError, TypeError):
            raise ValidationError('tdata must be valid JSON')

    class Meta:
        # Additional metadata for schema registry
        script_name = "land-cover"
        description = "Land cover change analysis parameters"