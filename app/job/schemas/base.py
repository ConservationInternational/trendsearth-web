"""
Base marshmallow schemas containing common parameter definitions shared across scripts.

This base schema reuses te_schemas components wherever possible to avoid duplication.
te_schemas and GDAL are required dependencies for this code to work.
"""

from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from te_schemas.jobs import Job as TeJob
from te_schemas.aoi import AOI as TeAOI


class AOISchema(Schema):
    """Schema for Area of Interest parameters using te_schemas.aoi.AOI."""

    # AOI ID for database lookup
    aoi_id = fields.Int(required=True, validate=validate.Range(min=1))

    # Use te_schemas.aoi.AOI for geojson validation
    geojson = fields.Nested(TeAOI.Schema(), dump_only=True)

    # Legacy fields for backward compatibility with existing API
    geojsons = fields.Str(dump_only=True)  # JSON array of geojson objects
    crs = fields.Str(dump_only=True)  # WGS84 CRS string
    crosses_180th = fields.Bool(dump_only=True, load_default=False)


class TaskInfoSchema(Schema):
    """Schema for task information using te_schemas.jobs.Job field definitions."""

    # Reuse exact field definitions from te_schemas.jobs.Job
    job_schema = TeJob.Schema()
    task_name = job_schema.fields["task_name"]
    task_notes = job_schema.fields["task_notes"]


class DateRangeSchema(Schema):
    """Schema for date range parameters used by many scripts."""

    year_initial = fields.Int(
        required=True, validate=validate.Range(min=1900, max=2100)
    )
    year_final = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))

    @validates_schema
    def validate_date_range(self, data, **kwargs):
        """Validate that final year is after initial year."""
        if data["year_final"] <= data["year_initial"]:
            raise ValidationError("year_final must be greater than year_initial")


class BaseJobSchema(Schema):
    """Base schema that includes common parameters for all job types using te_schemas where applicable."""

    # AOI selection
    aoi_id = fields.Int(required=True, validate=validate.Range(min=1))

    # Task information using te_schemas.jobs.Job field definitions
    job_schema = TeJob.Schema()
    task_name = job_schema.fields["task_name"]
    task_notes = job_schema.fields["task_notes"]

    # Derived fields that will be populated during processing
    geojsons = fields.Str(dump_only=True)  # Populated from AOI
    crs = fields.Str(dump_only=True)  # Set to default CRS
    crosses_180th = fields.Bool(dump_only=True, load_default=False)

    def load_and_populate_aoi(self, data):
        """
        Helper method to load AOI data and populate geometry fields using te_schemas.aoi.AOI.
        Should be called by subclass schemas during processing.
        """
        # This will be implemented to fetch AOI from database and populate geojsons
        pass
