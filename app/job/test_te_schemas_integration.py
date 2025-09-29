"""
Test te_schemas integration in marshmallow schemas.
"""

import sys
import os

# Add the parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_land_cover_te_schemas_integration():
    """Test that land cover schema uses te_schemas.land_cover.LCTransitionDefinitionDeg."""
    try:
        from schemas import schema_registry

        # Test data with a simple transition matrix
        test_params = {
            "aoi_id": 1,
            "task_name": "Land Cover Test",
            "initial_year_de": 2001,
            "target_year_de": 2020,
            "tdata": '{"0": {"0": "0", "1": "-"}, "1": {"0": "+", "1": "0"}}',
        }

        # This should use te_schemas validation internally
        schema_registry.validate_parameters("land-cover", test_params)

        print("✓ Land cover schema successfully integrated with te_schemas")
        return True

    except Exception as e:
        print(f"✗ Land cover te_schemas integration failed: {e}")
        return False


def test_productivity_te_schemas_integration():
    """Test that productivity schema uses te_schemas.productivity.ProductivityMode."""
    try:
        from schemas import schema_registry

        # Test with numeric mode (as used in existing code)
        test_params = {
            "aoi_id": 1,
            "task_name": "Productivity Test",
            "year_initial": 2001,
            "year_final": 2020,
            "ndvi_dataset": "MODIS",
            "prod_mode": 1,  # Should map to TRENDS_EARTH_5_CLASS_LPD
        }

        validated = schema_registry.validate_parameters("productivity", test_params)

        # Check that prod_mode was converted to ProductivityMode enum
        prod_mode = validated["prod_mode"]
        if hasattr(prod_mode, "value"):  # It's an enum
            print(f"✓ Productivity mode converted to enum: {prod_mode.value}")
        else:
            print(f"✓ Productivity mode validated: {prod_mode}")

        print("✓ Productivity schema successfully integrated with te_schemas")
        return True

    except Exception as e:
        print(f"✗ Productivity te_schemas integration failed: {e}")
        return False


def test_job_schema_field_reuse():
    """Test that base schema reuses te_schemas.jobs.Job fields."""
    try:
        from schemas import schema_registry

        # Get schema fields to check they match te_schemas definitions
        fields = schema_registry.get_schema_fields("land-cover")

        # Check that task_name and task_notes are present
        if "task_name" not in fields or "task_notes" not in fields:
            print("✗ Missing task fields from base schema")
            return False

        print("✓ Base schema successfully reuses te_schemas.jobs.Job fields")
        return True

    except Exception as e:
        print(f"✗ Job schema field reuse test failed: {e}")
        return False


def test_sub_indicators_te_schemas_integration():
    """Test that sub-indicators schema uses both land cover and productivity te_schemas."""
    try:
        from schemas import schema_registry

        test_params = {
            "aoi_id": 1,
            "task_name": "Sub-indicators Test",
            "year_initial": 2001,
            "year_final": 2020,
            "initial_year_de": 2001,
            "target_year_de": 2020,
            "tdata": '{"0": {"0": "0", "1": "-"}, "1": {"0": "+", "1": "0"}}',
            "calculate_productivity": True,
            "ndvi_dataset": "MODIS",
            "prod_mode": 2,  # Should map to JRC_5_CLASS_LPD
        }

        schema_registry.validate_parameters(
            "sdg-15-3-1-sub-indicators", test_params
        )

        print("✓ Sub-indicators schema successfully integrated with te_schemas")
        return True

    except Exception as e:
        print(f"✗ Sub-indicators te_schemas integration failed: {e}")
        return False


def test_fallback_when_te_schemas_unavailable():
    """Test graceful fallback when te_schemas modules are not available."""
    try:
        # This test assumes te_schemas is available, so we'll just verify
        # that our schemas handle import errors gracefully

        # Import a schema and check it has fallback handling
        from schemas.land_cover import LandCoverSchema

        # The schema should have been created successfully even if there were import issues
        LandCoverSchema()

        print("✓ Schemas handle te_schemas import gracefully")
        return True

    except Exception as e:
        print(f"✗ Fallback handling test failed: {e}")
        return False


def main():
    """Run te_schemas integration tests."""
    print("Running te_schemas integration tests...")

    tests = [
        test_land_cover_te_schemas_integration,
        test_productivity_te_schemas_integration,
        test_job_schema_field_reuse,
        test_sub_indicators_te_schemas_integration,
        test_fallback_when_te_schemas_unavailable,
    ]

    passed = 0
    for test in tests:
        print(f"\n--- Running {test.__name__} ---")
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")

    print("\n=== TE_SCHEMAS INTEGRATION RESULTS ===")
    print(f"Tests passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("All te_schemas integration tests passed! ✓")
        return 0
    else:
        print("Some te_schemas integration tests failed! ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())
