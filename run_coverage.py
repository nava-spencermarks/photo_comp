#!/usr/bin/env python3
"""
Local script to run tests with coverage reporting.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_local_coverage():
    """Run comprehensive coverage locally."""
    project_root = Path(__file__).parent
    
    print("🧪 Running tests with coverage...")
    print("=" * 60)
    
    # Test commands to try
    commands = [
        # Try with pytest (preferred)
        [
            sys.executable, "-m", "pytest", 
            "--cov=src", "--cov=test",
            "--cov-report=term-missing", 
            "--cov-report=html", 
            "--cov-report=xml",
            "-v"
        ],
        # Fallback: run our test runner with coverage
        [
            sys.executable, "-m", "coverage", "run",
            "--source=src,test", 
            "-m", "pytest", "test/"
        ]
    ]
    
    success = False
    
    for i, cmd in enumerate(commands):
        try:
            print(f"Trying method {i+1}...")
            result = subprocess.run(cmd, cwd=project_root)
            
            if result.returncode == 0:
                success = True
                break
            else:
                print(f"Method {i+1} failed with return code {result.returncode}")
                
        except FileNotFoundError as e:
            print(f"Method {i+1} failed: {e}")
        except Exception as e:
            print(f"Method {i+1} failed: {e}")
    
    if not success:
        print("❌ All coverage methods failed. Trying basic test run...")
        # Fallback to our custom test runner
        os.chdir(project_root / "test")
        result = subprocess.run([sys.executable, "run_all_tests.py"])
        return result.returncode == 0
    
    # Generate coverage report if we got this far
    try:
        print("\n" + "=" * 60)
        print("📊 Generating coverage report...")
        
        # Try to generate text report
        subprocess.run([
            sys.executable, "-m", "coverage", "report", "--show-missing"
        ], cwd=project_root)
        
        # Check if HTML report was generated
        html_dir = project_root / "htmlcov"
        if html_dir.exists():
            print(f"\n✅ HTML coverage report generated: {html_dir / 'index.html'}")
            print("   Open this file in your browser to view detailed coverage")
        
        # Check if XML report was generated  
        xml_file = project_root / "coverage.xml"
        if xml_file.exists():
            print(f"✅ XML coverage report generated: {xml_file}")
            
    except Exception as e:
        print(f"⚠️  Could not generate coverage report: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Coverage analysis complete!")
    
    return True

if __name__ == "__main__":
    success = run_local_coverage()
    sys.exit(0 if success else 1)