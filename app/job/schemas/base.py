"""
Base marshmallow schemas containing common parameter definitions shared across scripts.
"""

from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from marshmallow_dataclass import dataclass
import json


class AOISchema(Schema):
    """Schema for Area of Interest parameters common to all scripts."""
    aoi_id = fields.Int(required=True, validate=validate.Range(min=1))
    geojsons = fields.Str(required=True)
    crs = fields.Str(load_default='GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]')
    crosses_180th = fields.Bool(load_default=False)

    @validates_schema
    def validate_geojsons(self, data, **kwargs):
        """Validate that geojsons field contains valid JSON."""
        try:
            geojsons = json.loads(data['geojsons'])
            if not isinstance(geojsons, list):
                raise ValidationError('geojsons must be a JSON array')
        except (json.JSONDecodeError, TypeError):
            raise ValidationError('geojsons must be valid JSON')


class TaskInfoSchema(Schema):
    """Schema for task information common to all scripts."""
    task_name = fields.Str(required=True, validate=validate.Length(min=1, max=250))
    task_notes = fields.Str(load_default="", validate=validate.Length(max=1000))


class DateRangeSchema(Schema):
    """Schema for date range parameters used by many scripts."""
    year_initial = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))
    year_final = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))

    @validates_schema
    def validate_date_range(self, data, **kwargs):
        """Validate that final year is after initial year."""
        if data['year_final'] <= data['year_initial']:
            raise ValidationError('year_final must be greater than year_initial')


class BaseJobSchema(Schema):
    """Base schema that includes common parameters for all job types."""
    # Include common parameter groups
    aoi_id = fields.Int(required=True, validate=validate.Range(min=1))
    task_name = fields.Str(required=True, validate=validate.Length(min=1, max=250))
    task_notes = fields.Str(load_default="", validate=validate.Length(max=1000))
    
    # Derived fields that will be populated during processing
    geojsons = fields.Str(dump_only=True)  # Populated from AOI
    crs = fields.Str(dump_only=True)       # Set to default CRS
    crosses_180th = fields.Bool(dump_only=True, load_default=False)

    def load_and_populate_aoi(self, data):
        """
        Helper method to load AOI data and populate geometry fields.
        Should be called by subclass schemas during processing.
        """
        # This will be implemented to fetch AOI from database and populate geojsons
        pass