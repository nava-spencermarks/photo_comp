#!/usr/bin/env python3
"""
Run all tests for the face comparison system.
"""

import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_all_tests():
    """Run all test suites."""
    print("🧪 RUNNING ALL TESTS FOR FACE COMPARISON SYSTEM")
    print("=" * 60)
    
    test_modules = [
        ('test_robust_face_compare', 'Robust Face Comparison Tests'),
        ('test_main', 'Main Script Tests'),
    ]
    
    all_passed = True
    results = {}
    
    for module_name, description in test_modules:
        print(f"\n📋 {description}")
        print("-" * 40)
        
        try:
            # Import and run the test module
            module = __import__(module_name)
            if hasattr(module, 'run_tests'):
                passed = module.run_tests()
                results[description] = passed
                if not passed:
                    all_passed = False
            else:
                print(f"⚠️  No run_tests() function found in {module_name}")
                results[description] = False
                all_passed = False
                
        except ImportError as e:
            print(f"❌ Could not import {module_name}: {e}")
            results[description] = False
            all_passed = False
        except Exception as e:
            print(f"❌ Error running tests in {module_name}: {e}")
            results[description] = False
            all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    print("=" * 60)
    
    for description, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {description}")
    
    print("-" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("Your face comparison system is working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Please review the output above for details.")
    
    print("\n💡 To run individual test suites:")
    print("   python test_robust_face_compare.py")
    print("   python test_main.py")
    
    return all_passed

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)