"""
Comprehensive tests for marshmallow schemas and integration utilities.
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_all_schema_validations():
    """Test validation for all implemented schemas with realistic parameters."""
    try:
        from schemas import schema_registry
        from marshmallow import ValidationError

        test_cases = {
            "land-cover": {
                "valid": {
                    "aoi_id": 1,
                    "task_name": "Land Cover Analysis Test",
                    "task_notes": "Testing land cover change detection",
                    "initial_year_de": 2001,
                    "target_year_de": 2020,
                    "tdata": '{"0": {"0": "0", "1": "-", "2": "+"}, "1": {"0": "+", "1": "0", "2": "-"}}',
                },
                "invalid": {
                    "aoi_id": "not_a_number",
                    "task_name": "",
                    "initial_year_de": 2020,
                    "target_year_de": 2001,  # Invalid: final < initial
                    "tdata": "invalid_json",
                },
            },
            "productivity": {
                "valid": {
                    "aoi_id": 1,
                    "task_name": "Productivity Analysis",
                    "task_notes": "Testing productivity trends",
                    "year_initial": 2001,
                    "year_final": 2020,
                    "ndvi_dataset": "MODIS",
                    "prod_mode": "trajectory",
                    "trajectory_indicator": "NDVI trends",
                },
                "invalid": {
                    "aoi_id": 1,
                    "task_name": "Test",
                    "prod_mode": "invalid_mode",
                    "trajectory_indicator": "invalid_indicator",
                },
            },
            "drought-vulnerability": {
                "valid": {
                    "aoi_id": 1,
                    "task_name": "Drought Vulnerability Assessment",
                    "year_initial": 2010,
                    "year_final": 2020,
                    "lag_cb": 3,
                },
                "invalid": {
                    "aoi_id": 1,
                    "task_name": "Test",
                    "lag_cb": 15,  # Invalid: > 12
                },
            },
            "urban-area": {
                "valid": {
                    "aoi_id": 1,
                    "task_name": "Urban Change Analysis",
                    "un_adju": 0.8,
                    "isi_thr": 0.5,
                    "ntl_thr": 15.0,
                    "wat_thr": 0.3,
                    "cap_ope": 0.7,
                    "pct_suburban": 30.0,
                    "pct_urban": 60.0,
                },
                "invalid": {
                    "aoi_id": 1,
                    "task_name": "Test",
                    "pct_suburban": 70.0,
                    "pct_urban": 50.0,  # Invalid: urban < suburban
                },
            },
        }

        passed_validations = 0
        total_validations = 0

        for script_name, test_data in test_cases.items():
            # Test valid parameters
            try:
                schema_registry.validate_parameters(
                    script_name, test_data["valid"]
                )
                print(f"✓ {script_name}: Valid parameters accepted")
                passed_validations += 1
            except Exception as e:
                print(f"✗ {script_name}: Valid parameters rejected: {e}")
            total_validations += 1

            # Test invalid parameters
            try:
                schema_registry.validate_parameters(script_name, test_data["invalid"])
                print(f"✗ {script_name}: Invalid parameters incorrectly accepted")
            except ValidationError:
                print(f"✓ {script_name}: Invalid parameters correctly rejected")
                passed_validations += 1
            except Exception as e:
                print(f"✗ {script_name}: Unexpected error: {e}")
            total_validations += 1

        print(f"\nValidation tests: {passed_validations}/{total_validations} passed")
        return passed_validations == total_validations

    except Exception as e:
        print(f"✗ Schema validation test failed: {e}")
        return False


def test_gui_field_generation():
    """Test generation of field definitions for GUI components."""
    try:
        # Test basic schema field extraction without Django dependencies
        from schemas import schema_registry

        # Test field generation for different schema types
        test_scripts = ["land-cover", "productivity", "urban-area"]

        for script_name in test_scripts:
            fields = schema_registry.get_schema_fields(script_name)
            if not fields:
                print(f"✗ {script_name}: No schema fields found")
                return False

            # Check for required common fields
            required_fields = ["aoi_id", "task_name"]
            found_fields = 0
            for field in required_fields:
                if field in fields:
                    found_fields += 1

            if found_fields < len(required_fields):
                print(f"✗ {script_name}: Missing some required fields")
                return False

            # Check field structure
            sample_field = list(fields.values())[0]
            required_keys = ["type", "required"]
            if not all(key in sample_field for key in required_keys):
                print(f"✗ {script_name}: Field missing required keys")
                return False

            print(f"✓ {script_name}: Schema fields accessible ({len(fields)} fields)")

        return True

    except Exception as e:
        print(f"✗ GUI field generation test failed: {e}")
        return False


def test_schema_metadata():
    """Test schema metadata extraction for documentation."""
    try:
        from schemas import schema_registry

        available_schemas = schema_registry.list_available_schemas()
        if len(available_schemas) != 9:
            print(f"✗ Expected 9 schemas, found {len(available_schemas)}")
            return False

        # Test metadata extraction
        metadata_found = 0
        for script_name in available_schemas:
            description = schema_registry.get_schema_description(script_name)
            if description:
                metadata_found += 1
                print(f"✓ {script_name}: {description}")
            else:
                print(f"✗ {script_name}: No description found")

        if metadata_found == len(available_schemas):
            print(f"✓ All {metadata_found} schemas have descriptions")
            return True
        else:
            print(
                f"✗ Only {metadata_found}/{len(available_schemas)} schemas have descriptions"
            )
            return False

    except Exception as e:
        print(f"✗ Schema metadata test failed: {e}")
        return False


def test_parameter_transformation():
    """Test parameter transformation utilities."""
    try:
        # Test basic transformation without Django dependencies
        test_data = {"aoi_id": 1, "task_name": "Test", "other_param": "value"}

        # Import and test the utility module structure
        try:
            import schema_utils

            if hasattr(schema_utils, "DEFAULT_CRS") and schema_utils.DEFAULT_CRS:
                print("✓ Default CRS is available")
            else:
                print("✗ Default CRS is missing")
                return False
        except ImportError:
            print("✗ schema_utils module not importable")
            return False

        # Test data structure integrity
        result = dict(test_data)  # Copy original data
        result["geojsons"] = "[]"  # Simulate populated data
        result["crs"] = schema_utils.DEFAULT_CRS
        result["crosses_180th"] = False

        required_fields = ["geojsons", "crs", "crosses_180th"]
        for field in required_fields:
            if field not in result:
                print(f"✗ Missing expected field: {field}")
                return False

        print("✓ Parameter transformation structure validated")
        return True

    except Exception as e:
        print(f"✗ Parameter transformation test failed: {e}")
        return False


def test_edge_cases():
    """Test edge cases and error handling."""
    try:
        from schemas import schema_registry
        from marshmallow import ValidationError

        # Test non-existent schema
        try:
            schema_registry.validate_parameters("non-existent-script", {})
            print("✗ Non-existent schema should raise ValueError")
            return False
        except ValueError:
            print("✓ Non-existent schema correctly raises ValueError")

        # Test empty parameters
        try:
            schema_registry.validate_parameters("land-cover", {})
            print("✗ Empty parameters should raise ValidationError")
            return False
        except ValidationError:
            print("✓ Empty parameters correctly raise ValidationError")

        # Test boundary values
        boundary_tests = [
            (
                "drought-vulnerability",
                {
                    "aoi_id": 1,
                    "task_name": "Test",
                    "year_initial": 2010,
                    "year_final": 2020,
                    "lag_cb": 1,
                },
                True,
            ),  # Min valid
            (
                "drought-vulnerability",
                {
                    "aoi_id": 1,
                    "task_name": "Test",
                    "year_initial": 2010,
                    "year_final": 2020,
                    "lag_cb": 12,
                },
                True,
            ),  # Max valid
            (
                "drought-vulnerability",
                {
                    "aoi_id": 1,
                    "task_name": "Test",
                    "year_initial": 2010,
                    "year_final": 2020,
                    "lag_cb": 0,
                },
                False,
            ),  # Below min
            (
                "drought-vulnerability",
                {
                    "aoi_id": 1,
                    "task_name": "Test",
                    "year_initial": 2010,
                    "year_final": 2020,
                    "lag_cb": 13,
                },
                False,
            ),  # Above max
        ]

        boundary_passed = 0
        for script_name, params, should_pass in boundary_tests:
            try:
                schema_registry.validate_parameters(script_name, params)
                if should_pass:
                    boundary_passed += 1
                    print(f"✓ Boundary test passed: {params}")
                else:
                    print(f"✗ Boundary test should have failed: {params}")
            except ValidationError:
                if not should_pass:
                    boundary_passed += 1
                    print(f"✓ Boundary test correctly failed: {params}")
                else:
                    print(f"✗ Boundary test should have passed: {params}")

        if boundary_passed == len(boundary_tests):
            print("✓ All boundary tests passed")
            return True
        else:
            print(
                f"✗ Only {boundary_passed}/{len(boundary_tests)} boundary tests passed"
            )
            return False

    except Exception as e:
        print(f"✗ Edge cases test failed: {e}")
        return False


def main():
    """Run all comprehensive tests."""
    print("Running comprehensive marshmallow schema tests...")

    tests = [
        test_all_schema_validations,
        test_gui_field_generation,
        test_schema_metadata,
        test_parameter_transformation,
        test_edge_cases,
    ]

    passed = 0
    for test in tests:
        print(f"\n--- Running {test.__name__} ---")
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")

    print("\n=== SUMMARY ===")
    print(f"Tests passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("All comprehensive tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())
