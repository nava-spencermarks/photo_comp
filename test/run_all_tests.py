#!/usr/bin/env python3
"""
Run all tests for the face comparison system.
"""

import os
import sys

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
    detailed_results = {}
    
    for module_name, description in test_modules:
        print(f"\n📋 {description}")
        print("-" * 40)
        
        try:
            # Import the test module
            module = __import__(module_name)
            
            # Run tests with detailed reporting
            import unittest
            import io
            
            # Create a test suite
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(module)
            
            # Capture output
            stream = io.StringIO()
            runner = unittest.TextTestRunner(stream=stream, verbosity=2)
            result = runner.run(suite)
            
            # Parse results
            test_output = stream.getvalue()
            passed = result.wasSuccessful()
            
            results[description] = passed
            detailed_results[description] = {
                'total': result.testsRun,
                'passed': result.testsRun - len(result.failures) - len(result.errors),
                'failed': len(result.failures),
                'errors': len(result.errors),
                'details': result
            }
            
            # Show summary for this module
            print(f"Tests run: {result.testsRun}")
            print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
            if result.failures:
                print(f"❌ Failed: {len(result.failures)}")
            if result.errors:
                print(f"💥 Errors: {len(result.errors)}")
                
            # Show individual test results
            if result.failures or result.errors:
                print("\nFailed Tests:")
                for test, traceback in result.failures:
                    print(f"  ❌ {test}")
                for test, traceback in result.errors:
                    print(f"  💥 {test}")
            
            if not passed:
                all_passed = False
                
        except ImportError as e:
            print(f"❌ Could not import {module_name}: {e}")
            results[description] = False
            detailed_results[description] = {'total': 0, 'passed': 0, 'failed': 1, 'errors': 0}
            all_passed = False
        except Exception as e:
            print(f"❌ Error running tests in {module_name}: {e}")
            results[description] = False
            detailed_results[description] = {'total': 0, 'passed': 0, 'failed': 0, 'errors': 1}
            all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    print("DETAILED TEST SUMMARY:")
    print("=" * 60)
    
    total_tests = 0
    total_passed = 0
    total_failed = 0
    total_errors = 0
    
    for description, passed in results.items():
        details = detailed_results[description]
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {description}")
        print(f"    Tests: {details['total']} | Passed: {details['passed']} | Failed: {details['failed']} | Errors: {details['errors']}")
        
        total_tests += details['total']
        total_passed += details['passed']
        total_failed += details['failed']
        total_errors += details['errors']
    
    print("-" * 60)
    print(f"OVERALL: {total_tests} tests | ✅ {total_passed} passed | ❌ {total_failed} failed | 💥 {total_errors} errors")
    print("-" * 60)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("Your face comparison system is working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Please review the failed tests above for details.")
    
    print("\n💡 To run individual test suites:")
    print("   python test_face_compare.py")
    print("   python test_main.py")
    
    return all_passed

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)