#!/usr/bin/env python3
"""
Coverage tracking and baseline management for the face comparison project.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
import argparse


class CoverageTracker:
    def __init__(self):
        self.baseline_file = Path(".coverage_baseline.json")
        self.project_root = Path(__file__).parent

    def run_coverage(self):
        """Run tests with coverage and return coverage percentage."""
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "--cov=src",
            "--cov=test",
            "--cov-report=term-missing",
            "--cov-report=xml",
            "--quiet",
        ]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.project_root
            )

            # Extract coverage percentage from output
            match = re.search(r"TOTAL.*?(\d+)%", result.stdout)
            coverage_percent = float(match.group(1)) if match else 0.0

            return coverage_percent, result.stdout
        except Exception as e:
            print(f"Error running coverage: {e}")
            return 0.0, ""

    def get_baseline(self):
        """Get baseline coverage from file."""
        try:
            if self.baseline_file.exists():
                with open(self.baseline_file) as f:
                    data = json.load(f)
                    return data.get("total_coverage", 0.0)
        except Exception as e:
            print(f"Warning: Could not read baseline: {e}")

        return None

    def set_baseline(self, coverage_percent):
        """Set new baseline coverage."""
        baseline_data = {
            "total_coverage": coverage_percent,
            "timestamp": subprocess.run(
                ["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True
            ).stdout.strip(),
        }

        try:
            with open(self.baseline_file, "w") as f:
                json.dump(baseline_data, f, indent=2)
            print(f"✅ Baseline set to {coverage_percent}%")
        except Exception as e:
            print(f"Error setting baseline: {e}")

    def check_coverage_regression(self, tolerance=2.0):
        """Check if coverage has regressed beyond tolerance."""
        current_coverage, output = self.run_coverage()
        baseline_coverage = self.get_baseline()

        print(f"\n📊 Coverage Report:")
        print(f"Current Coverage: {current_coverage}%")

        if baseline_coverage is not None:
            print(f"Baseline Coverage: {baseline_coverage}%")
            diff = current_coverage - baseline_coverage
            print(f"Change: {diff:+.1f}%")

            if diff >= 0:
                print("✅ Coverage maintained or improved")
                return True
            elif abs(diff) <= tolerance:
                print(f"📊 Coverage within tolerance ({tolerance}%)")
                return True
            else:
                print(f"❌ Coverage regression exceeds tolerance ({tolerance}%)")
                print("Consider:")
                print("  - Adding tests for new code")
                print("  - Improving existing test coverage")
                return False
        else:
            print("⚠️  No baseline found - setting current coverage as baseline")
            self.set_baseline(current_coverage)
            return True

    def reset_baseline(self):
        """Reset baseline to current coverage."""
        coverage_percent, _ = self.run_coverage()
        self.set_baseline(coverage_percent)
        return coverage_percent


def main():
    parser = argparse.ArgumentParser(description="Track code coverage")
    parser.add_argument(
        "--reset-baseline",
        action="store_true",
        help="Reset baseline to current coverage",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=2.0,
        help="Coverage regression tolerance (default: 2.0%%)",
    )

    args = parser.parse_args()

    tracker = CoverageTracker()

    if args.reset_baseline:
        coverage = tracker.reset_baseline()
        print(f"Baseline reset to {coverage}%")
        return 0
    else:
        success = tracker.check_coverage_regression(args.tolerance)
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
