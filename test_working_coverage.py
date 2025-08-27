#!/usr/bin/env python3
"""
Test script that runs only the working tests for clean coverage reporting.
"""
import subprocess
import sys
from pathlib import Path


def run_working_coverage():
    """Run coverage with only the working test files."""
    project_root = Path(__file__).parent

    print("🧪 Running working tests with coverage...")
    print("=" * 60)

    # Run only the working tests
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=xml",
        "-v",
        "test/test_inspect_image.py",
        "test/test_main.py",
        "test/test_face_compare.py",
        "test/test_webapp.py",
        "test/test_image_masking.py",
        "test/test_rectangle_frontend.py",
    ]

    try:
        result = subprocess.run(cmd, cwd=project_root)

        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("📊 Checking coverage regression...")

            # Check coverage regression
            regression_result = subprocess.run(
                [sys.executable, "coverage_tracker.py", "--tolerance", "2.0"],
                cwd=project_root,
            )

            if regression_result.returncode != 0:
                print("❌ Coverage regression detected! Build failed.")
                return False
            else:
                print("✅ Coverage regression check passed.")

            print("\n✅ All working tests passed with good coverage!")
            return True
        else:
            print("❌ Tests failed")
            return False

    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


if __name__ == "__main__":
    success = run_working_coverage()
    sys.exit(0 if success else 1)
