# Data Files Directory

This directory contains configuration and schema data files for the Trends.Earth web application.

## Land Cover Schema Files (DEPRECATED)

⚠️ **These files are deprecated and should be removed once te_schemas is properly installed:**

- `land_cover_transition_matrix_unccd.json` - Default UNCCD land cover transition matrix
- `land_cover_nesting_unccd_esa.json` - Default UNCCD/ESA land cover nesting

These files duplicate data that is available in the `te_schemas` package. The application now uses a compatibility layer (`utils.schemas_compat`) that prefers `te_schemas` data when available and falls back to these local files.

**Migration path:**
1. Install `te_schemas` as a dependency
2. Verify compatibility layer works with `te_schemas`
3. Remove these files
4. Update compatibility layer to use only `te_schemas` defaults

## Application-Specific Configuration Files

These files contain configuration specific to the web application:

- `scripts.json` - Script/algorithm definitions for the web interface
- `gee_datasets.json` - Google Earth Engine dataset configurations
- `styles.json` - Map styling configurations

These files are NOT duplicated in other repositories as they contain web-application-specific configurations.

## See Also

- `../schemas_compat.py` - Compatibility layer for te_schemas integration
- `../conf.py` - Algorithm configuration and settings management
- `../../SCHEMAS_MIGRATION.md` - Complete migration plan documentation