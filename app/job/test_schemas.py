"""
Simple tests for marshmallow schemas to validate basic functionality.
"""

import json
import sys
import os

# Add the parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_schema_imports():
    """Test that all schemas can be imported successfully."""
    try:
        from schemas import (
            BaseJobSchema, LandCoverSchema, ProductivitySchema,
            DroughtVulnerabilitySchema, UrbanChangeSchema, UNCCDReportingSchema,
            RestorationBiomassSchema, SoilCarbonSchema, TotalCarbonSchema,
            SubIndicatorsSchema, schema_registry
        )
        print("✓ All schema imports successful")
        return True
    except ImportError as e:
        print(f"✗ Schema import failed: {e}")
        return False

def test_schema_registry():
    """Test that schema registry works correctly."""
    try:
        from schemas import schema_registry
        
        # Test listing available schemas
        available = schema_registry.list_available_schemas()
        print(f"✓ Schema registry has {len(available)} schemas: {available}")
        
        # Test getting a specific schema
        productivity_schema = schema_registry.get_schema_instance('productivity')
        if productivity_schema:
            print("✓ Successfully retrieved productivity schema")
        else:
            print("✗ Failed to retrieve productivity schema")
            return False
            
        # Test getting schema fields for GUI generation
        fields = schema_registry.get_schema_fields('land-cover')
        if fields and 'aoi_id' in fields:
            print(f"✓ Successfully retrieved schema fields ({len(fields)} fields)")
        else:
            print("✗ Failed to retrieve schema fields")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Schema registry test failed: {e}")
        return False

def test_basic_validation():
    """Test basic parameter validation."""
    try:
        from schemas import schema_registry
        
        # Test land cover schema validation
        land_cover_params = {
            'aoi_id': 1,
            'task_name': 'Test Land Cover Analysis',
            'task_notes': 'Test run',
            'initial_year_de': 2001,
            'target_year_de': 2020,
            'tdata': '{"test": "data"}'
        }
        
        validated = schema_registry.validate_parameters('land-cover', land_cover_params)
        if validated['aoi_id'] == 1 and validated['task_name'] == 'Test Land Cover Analysis':
            print("✓ Land cover schema validation successful")
        else:
            print("✗ Land cover schema validation failed")
            return False
            
        # Test validation error handling
        invalid_params = {
            'aoi_id': 'invalid',  # Should be integer
            'task_name': '',      # Should not be empty
        }
        
        try:
            schema_registry.validate_parameters('land-cover', invalid_params)
            print("✗ Validation should have failed for invalid parameters")
            return False
        except Exception:
            print("✓ Validation correctly rejected invalid parameters")
            
        return True
    except Exception as e:
        print(f"✗ Basic validation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Running marshmallow schema tests...")
    
    tests = [
        test_schema_imports,
        test_schema_registry,
        test_basic_validation,
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
    
    print(f"\nTests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1

if __name__ == '__main__':
    sys.exit(main())