# Migration to te_schemas and te_algorithms

This document outlines the migration plan to eliminate duplication between this repository and the `trends.earth-schemas` and `trends.earth-algorithms` repositories.

## Current State

As of this migration, the codebase was importing from `te_schemas` and `te_algorithms` packages but these were not available as dependencies, causing import failures. Additionally, several data files were duplicated between repositories.

## Changes Made

### 1. Compatibility Layer (`utils/schemas_compat.py`)

Created a compatibility layer that:
- Attempts to import from `te_schemas` when available
- Falls back to local data files when `te_schemas` is not available
- Provides stub classes for backward compatibility
- Prepares for proper package usage when dependencies become available

### 2. Updated Imports

All direct imports from `te_schemas` have been replaced with imports from the compatibility layer:

**Before:**
```python
from te_schemas.land_cover import LCTransitionDefinitionDeg
from te_schemas.productivity import ProductivityMode
```

**After:**
```python
from utils.schemas_compat import LCTransitionDefinitionDeg, ProductivityMode
```

### 3. Enhanced Data Loading Functions

Updated `utils/util.py` functions to prefer `te_schemas` data over local files:
- `get_trans_matrix()` - now tries `te_schemas` first
- `get_lc_nesting()` - now tries `te_schemas` first
- Added deprecation warnings for local data file usage

## Files That Should Be Removed (Future)

Once `te_schemas` and `te_algorithms` are properly installed as dependencies, the following duplicate data files can be removed:

### Land Cover Data (duplicated in te_schemas)
- `app/utils/data/land_cover_transition_matrix_unccd.json`
- `app/utils/data/land_cover_nesting_unccd_esa.json`

These files contain the same data that is available in the `te_schemas` package.

### Algorithm Configurations (potentially duplicated in te_algorithms)
- `app/utils/data/scripts.json` - May contain algorithm definitions that exist in `te_algorithms`
- Parts of `app/utils/conf.py` - Algorithm configuration logic that may overlap with `te_algorithms`

## Next Steps

### Phase 1: Install Dependencies (When Available)
1. Update `requirements.txt` to include proper versions:
   ```
   te_schemas>=2.1.17
   te_algorithms>=2.1.17
   ```

2. Test that imports work correctly with real packages

### Phase 2: Remove Duplicate Data Files
1. Verify that `te_schemas` provides equivalent data for:
   - Land cover transition matrices
   - Land cover nesting definitions
   
2. Remove local data files and update compatibility layer to use `te_schemas` defaults

3. Test that all functionality continues to work

### Phase 3: Algorithm Integration
1. Review `utils/conf.py` and `utils/data/scripts.json` against `te_algorithms`
2. Identify and remove duplicate algorithm definitions
3. Update algorithm loading to use `te_algorithms` where appropriate

### Phase 4: Clean Up
1. Remove compatibility layer once `te_schemas` is required dependency
2. Update all imports to use `te_schemas` and `te_algorithms` directly
3. Remove deprecated functions in `utils/util.py`

## Testing

After each phase, ensure:
- All smoke tests pass: `python test_simple.py`
- Django can import all modules without errors
- Land cover functionality works correctly
- Algorithm definitions load properly

## Benefits

This migration will:
- Eliminate code duplication across repositories
- Ensure consistency of schemas and algorithms
- Reduce maintenance burden
- Make updates to schemas/algorithms automatic when packages are updated
- Follow proper dependency management practices