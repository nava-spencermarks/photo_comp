#!/usr/bin/env python3
"""
Linting script that runs flake8, black, and isort checks.
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"🔍 {description}...")
    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
            
        if result.returncode == 0:
            print(f"✅ {description} passed")
            return True
        else:
            print(f"❌ {description} failed (exit code: {result.returncode})")
            return False
            
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        print(f"Please install it with: pip install {cmd[0]}")
        return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    """Run all linting checks."""
    project_root = Path(__file__).parent
    
    print("🧹 RUNNING CODE LINTING CHECKS")
    print("=" * 60)
    
    # Define source directories
    src_dirs = ["src", "test"]
    src_files = []
    for src_dir in src_dirs:
        src_path = project_root / src_dir
        if src_path.exists():
            src_files.extend(str(f) for f in src_path.rglob("*.py"))
    
    if not src_files:
        print("❌ No Python files found to lint")
        return False
    
    print(f"Linting {len(src_files)} Python files in: {', '.join(src_dirs)}")
    print()
    
    all_passed = True
    
    # 1. Check import sorting with isort
    isort_cmd = [sys.executable, "-m", "isort", "--check-only", "--diff"] + src_files
    if not run_command(isort_cmd, "Import sorting check (isort)"):
        all_passed = False
        print("💡 To fix import sorting issues, run: python -m isort src test")
        print()
    
    # 2. Check code formatting with black
    black_cmd = [sys.executable, "-m", "black", "--check", "--diff"] + src_files
    if not run_command(black_cmd, "Code formatting check (black)"):
        all_passed = False
        print("💡 To fix formatting issues, run: python -m black src test")
        print()
    
    # 3. Check code style with flake8
    flake8_cmd = [sys.executable, "-m", "flake8"] + src_files
    if not run_command(flake8_cmd, "Code style check (flake8)"):
        all_passed = False
        print("💡 Fix flake8 issues manually or adjust .flake8 config")
        print()
    
    # Summary
    print("=" * 60)
    if all_passed:
        print("🎉 ALL LINTING CHECKS PASSED!")
        print("Your code follows proper style guidelines.")
    else:
        print("⚠️  LINTING CHECKS FAILED")
        print("Please fix the issues above before running tests.")
        print()
        print("Quick fix commands:")
        print("  python -m black src test      # Fix formatting")
        print("  python -m isort src test      # Fix import sorting")
        print("  python -m flake8 src test     # Check remaining issues")
    
    print("=" * 60)
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)