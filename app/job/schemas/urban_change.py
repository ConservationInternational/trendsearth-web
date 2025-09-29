"""
Marshmallow schema for urban area change job parameters.
"""

from marshmallow import fields, validate, validates_schema, ValidationError
from .base import BaseJobSchema


class UrbanChangeSchema(BaseJobSchema):
    """Schema for urban area change script parameters."""

    # Urban area thresholds and parameters
    un_adju = fields.Float(
        required=True,
        validate=validate.Range(min=0.0, max=1.0),
        metadata={
            "title": "UN adjustment factor",
            "description": "Urban area adjustment factor",
        },
    )

    isi_thr = fields.Float(
        required=True,
        validate=validate.Range(min=0.0, max=1.0),
        metadata={
            "title": "ISI threshold",
            "description": "Impervious Surface Index threshold",
        },
    )

    ntl_thr = fields.Float(
        required=True,
        validate=validate.Range(min=0.0, max=100.0),
        metadata={
            "title": "NTL threshold",
            "description": "Night Time Lights threshold",
        },
    )

    wat_thr = fields.Float(
        required=True,
        validate=validate.Range(min=0.0, max=1.0),
        metadata={"title": "Water threshold", "description": "Water mask threshold"},
    )

    cap_ope = fields.Float(
        required=True,
        validate=validate.Range(min=0.0, max=1.0),
        metadata={
            "title": "Capture open areas",
            "description": "Factor for capturing open urban areas",
        },
    )

    pct_suburban = fields.Float(
        required=True,
        validate=validate.Range(min=0.0, max=100.0),
        metadata={
            "title": "Suburban percentage",
            "description": "Percentage threshold for suburban areas",
        },
    )

    pct_urban = fields.Float(
        required=True,
        validate=validate.Range(min=0.0, max=100.0),
        metadata={
            "title": "Urban percentage",
            "description": "Percentage threshold for urban areas",
        },
    )

    @validates_schema
    def validate_percentage_order(self, data, **kwargs):
        """Validate that urban percentage is higher than suburban percentage."""
        if data["pct_urban"] <= data["pct_suburban"]:
            raise ValidationError("pct_urban must be greater than pct_suburban")

    class Meta:
        script_name = "urban-area"
        description = "Urban area change analysis parameters"
