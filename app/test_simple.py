#!/usr/bin/env python3
"""
Simple smoke tests that don't require full Django setup.
These tests validate basic Python imports and syntax.
"""

import ast
import glob
import os


def test_basic_imports():
    """Test that basic Python modules can be imported."""
    try:
        # Test standard library imports that the app uses
        import json  # noqa: F401
        import sys  # noqa: F401
        import datetime  # noqa: F401
        import pathlib  # noqa: F401

        print("✓ Standard library imports successful")

        # Test that Django can be imported
        import django  # noqa: F401

        print("✓ Django import successful")

        # Test that app directory structure exists
        assert os.path.exists("core"), "Core app directory should exist"
        assert os.path.exists("job"), "Job app directory should exist"
        assert os.path.exists("account"), "Account app directory should exist"
        assert os.path.exists("utils"), "Utils directory should exist"
        assert os.path.exists("main"), "Main directory should exist"
        print("✓ App directory structure validated")

        return True
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False


def test_python_syntax():
    """Test that Python files have valid syntax."""
    python_files = glob.glob("**/*.py", recursive=True)
    failed_files = []

    for file_path in python_files:
        if "migrations" in file_path:
            continue  # Skip migration files

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            ast.parse(source)
        except SyntaxError as e:
            failed_files.append((file_path, str(e)))
        except Exception:
            # Skip files that can't be read (binary, etc.)
            continue

    if failed_files:
        print("✗ Syntax errors found:")
        for file_path, error in failed_files:
            print(f"  {file_path}: {error}")
        return False
    else:
        print(f"✓ All {len(python_files)} Python files have valid syntax")
        return True


def main():
    """Run all tests."""
    print("Running simple smoke tests...")

    tests = [
        test_basic_imports,
        test_python_syntax,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"Tests passed: {passed}/{total}")
    if passed == total:
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
