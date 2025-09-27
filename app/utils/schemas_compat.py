"""
Compatibility layer for te_schemas and te_algorithms packages.

This module provides backward compatibility when te_schemas and te_algorithms
packages are not available, while preparing for proper import usage.
"""
import os
import json
from typing import Optional, Any

# Try to import te_schemas, fall back to local data if not available
try:
    from te_schemas.land_cover import (
        LCLegendNesting,
        LCTransitionMeaningDeg,
        LCTransitionDefinitionDeg,
        LCTransitionMatrixDeg,
    )
    from te_schemas.productivity import ProductivityMode
    
    TE_SCHEMAS_AVAILABLE = True
except ImportError:
    TE_SCHEMAS_AVAILABLE = False
    
    # Minimal stubs for compatibility
    class ProductivityMode:
        TRENDS_EARTH_5_CLASS_LPD = "TrendsEarth-LPD-5"
        JRC_5_CLASS_LPD = "JRC-LPD-5"
        FAO_WOCAT_5_CLASS_LPD = "FAO-WOCAT-LPD-5"
    
    class LCTransitionDefinitionDeg:
        class Schema:
            def loads(self, data):
                # Return a minimal object that can be used by existing code
                return json.loads(data) if isinstance(data, str) else data


def get_default_land_cover_matrix():
    """
    Get the default land cover transition matrix.
    
    If te_schemas is available, this should use the built-in default matrix.
    Otherwise, fall back to local data file.
    """
    if TE_SCHEMAS_AVAILABLE:
        # TODO: Use te_schemas built-in default when available
        # For now, still use local file but through te_schemas classes
        pass
    
    # Fall back to local data file
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    matrix_file = os.path.join(data_dir, "land_cover_transition_matrix_unccd.json")
    
    try:
        with open(matrix_file) as f:
            matrix_data = json.load(f)
        
        if TE_SCHEMAS_AVAILABLE:
            return LCTransitionDefinitionDeg.Schema().loads(json.dumps(matrix_data))
        else:
            return matrix_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        from utils.logger import log
        log(f"Error loading land cover transition matrix from {matrix_file}: {e}")
        return None


def get_default_land_cover_nesting():
    """
    Get the default land cover nesting.
    
    If te_schemas is available, this should use the built-in default nesting.
    Otherwise, fall back to local data file.
    """
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    nesting_file = os.path.join(data_dir, "land_cover_nesting_unccd_esa.json")
    
    try:
        with open(nesting_file) as f:
            nesting_data = json.load(f)
        
        if TE_SCHEMAS_AVAILABLE:
            return LCLegendNesting.Schema().loads(json.dumps(nesting_data))
        else:
            return nesting_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        from utils.logger import log
        log(f"Error loading land cover nesting from {nesting_file}: {e}")
        return None


# Export the classes/functions that other modules expect
if TE_SCHEMAS_AVAILABLE:
    __all__ = [
        'LCLegendNesting',
        'LCTransitionMeaningDeg', 
        'LCTransitionDefinitionDeg',
        'LCTransitionMatrixDeg',
        'ProductivityMode',
        'get_default_land_cover_matrix',
        'get_default_land_cover_nesting',
        'TE_SCHEMAS_AVAILABLE'
    ]
else:
    __all__ = [
        'ProductivityMode',
        'LCTransitionDefinitionDeg',
        'get_default_land_cover_matrix',
        'get_default_land_cover_nesting',
        'TE_SCHEMAS_AVAILABLE'
    ]