# Temporary compatibility stubs for te_schemas


class ProductivityMode:
    """Compatibility stub for ProductivityMode"""

    TRENDS_EARTH_5_CLASS_LPD = "trends_earth_5_class_lpd"
    JRC_5_CLASS_LPD = "jrc_5_class_lpd"


class LCTransitionDefinitionDeg:
    """Compatibility stub for LCTransitionDefinitionDeg"""

    class Schema:
        def dumps(self, data):
            import json

            return json.dumps(data)
