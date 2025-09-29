"""
Marshmallow schema for land productivity job parameters.

This schema reuses te_schemas.productivity.ProductivityMode for
productivity mode validation to maintain consistency with existing code.
te_schemas and GDAL are required dependencies for this code to work.
"""

from marshmallow import fields, validate, validates_schema, ValidationError
from .base import BaseJobSchema, DateRangeSchema

from te_schemas.productivity import ProductivityMode


class ProductivityModeField(fields.Field):
    """Custom field for ProductivityMode validation using te_schemas."""

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, ProductivityMode):
            return value.value
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        # Handle both enum values and raw strings
        if isinstance(value, str):
            # Try to match by value first
            for mode in ProductivityMode:
                if mode.value == value:
                    return mode

            # Try to match by name (case insensitive)
            try:
                return ProductivityMode[value.upper()]
            except KeyError:
                pass

            # Handle legacy values from frontend
            legacy_mapping = {
                "state": ProductivityMode.TRENDS_EARTH_5_CLASS_LPD,
                "performance": ProductivityMode.TRENDS_EARTH_5_CLASS_LPD,
                "trajectory": ProductivityMode.TRENDS_EARTH_5_CLASS_LPD,
                "all": ProductivityMode.TRENDS_EARTH_5_CLASS_LPD,
            }
            if value in legacy_mapping:
                return legacy_mapping[value]

        # If numeric value (as seen in existing code)
        if isinstance(value, (int, str)) and str(value).isdigit():
            mode_mapping = {
                1: ProductivityMode.TRENDS_EARTH_5_CLASS_LPD,
                2: ProductivityMode.JRC_5_CLASS_LPD,
                3: ProductivityMode.FAO_WOCAT_5_CLASS_LPD,
            }
            mode_id = int(value)
            if mode_id in mode_mapping:
                return mode_mapping[mode_id]

        raise ValidationError(
            f"Invalid productivity mode: {value}. Valid options: {[mode.value for mode in ProductivityMode]}"
        )


class ProductivitySchema(BaseJobSchema, DateRangeSchema):
    """Schema for land productivity script parameters using te_schemas validation."""

    # NDVI dataset selection
    ndvi_dataset = fields.Str(required=True, validate=validate.Length(min=1))

    # Productivity mode selection using te_schemas ProductivityMode
    prod_mode = ProductivityModeField(required=True)

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
        prod_mode = data.get("prod_mode")

        # Handle both enum and string values
        mode_str = prod_mode.value if hasattr(prod_mode, "value") else str(prod_mode)

        if mode_str in ["trajectory", "all"] or "trajectory" in mode_str.lower():
            if not data.get("trajectory_indicator"):
                raise ValidationError(
                    "trajectory_indicator is required for trajectory mode"
                )

        # Validate trajectory indicator values
        trajectory_indicator = data.get("trajectory_indicator")
        if trajectory_indicator:
            valid_indicators = [
                "NDVI trends",
                "Pixel RESTREND",
                "Rain Use Efficiency (RUE)",
                "Water Use Efficiency (WUE)",
            ]
            if trajectory_indicator not in valid_indicators:
                raise ValidationError(
                    f"trajectory_indicator must be one of: {valid_indicators}"
                )

    @validates_schema
    def validate_performance_params(self, data, **kwargs):
        """Validate performance-specific parameters when performance mode is selected."""
        prod_mode = data.get("prod_mode")

        # Handle both enum and string values
        mode_str = prod_mode.value if hasattr(prod_mode, "value") else str(prod_mode)

        if mode_str in ["performance", "all"] or "performance" in mode_str.lower():
            if not data.get("performance_n_years"):
                data["performance_n_years"] = 5  # Default value

    class Meta:
        script_name = "productivity"
        description = (
            "Land productivity analysis parameters using te_schemas validation"
        )
