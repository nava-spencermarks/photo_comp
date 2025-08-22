#!/usr/bin/env python3
"""
Extended tests for main.py to increase coverage.
"""

import unittest
import subprocess
import sys
import os
import tempfile
from PIL import Image
from unittest.mock import patch, MagicMock

class TestMainScriptExtended(unittest.TestCase):
    """Extended tests for main.py to cover more edge cases."""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def create_simple_image(self, filename):
        """Create a simple test image."""
        img = Image.new('RGB', (100, 100), color='white')
        path = os.path.join(self.test_dir, filename)
        img.save(path)
        return path
    
    def run_main_script(self, args):
        """Run the main script with given arguments."""
        script_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'main.py')
        cmd = [sys.executable, script_path] + args
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result
    
    def test_successful_comparison_same_person(self):
        """Test successful comparison that finds same person."""
        img1 = self.create_simple_image('same1.png')
        img2 = self.create_simple_image('same2.png')
        
        # Mock the FaceComparator to return same person
        with patch('src.main.FaceComparator') as mock_comparator_class:
            mock_comparator = MagicMock()
            mock_comparator.compare_faces.return_value = (
                True, 
                "Distance: 0.25, Confidence: 85.5%"
            )
            mock_comparator_class.return_value = mock_comparator
            
            result = self.run_main_script([img1, img2])
            
            # Should succeed and show same person result
            self.assertEqual(result.returncode, 0)
            self.assertIn("SAME PERSON", result.stdout)
    
    def test_successful_comparison_different_people(self):
        """Test successful comparison that finds different people."""
        img1 = self.create_simple_image('diff1.png')
        img2 = self.create_simple_image('diff2.png')
        
        # Mock the FaceComparator to return different people
        with patch('src.main.FaceComparator') as mock_comparator_class:
            mock_comparator = MagicMock()
            mock_comparator.compare_faces.return_value = (
                False, 
                "Distance: 0.75, Confidence: 0%"
            )
            mock_comparator_class.return_value = mock_comparator
            
            result = self.run_main_script([img1, img2])
            
            # Should succeed and show different people result
            self.assertEqual(result.returncode, 0)
            self.assertIn("DIFFERENT PEOPLE", result.stdout)
    
    def test_comparison_with_error_handling(self):
        """Test comparison when FaceComparator raises an exception."""
        img1 = self.create_simple_image('error1.png')
        img2 = self.create_simple_image('error2.png')
        
        # Mock the FaceComparator to raise an exception
        with patch('src.main.FaceComparator') as mock_comparator_class:
            mock_comparator = MagicMock()
            mock_comparator.compare_faces.side_effect = Exception("Comparison failed")
            mock_comparator_class.return_value = mock_comparator
            
            result = self.run_main_script([img1, img2])
            
            # Should handle the error gracefully (depending on implementation)
            # At minimum, should not return 0 or should have error output
            self.assertTrue(result.returncode != 0 or len(result.stderr) > 0 or "error" in result.stdout.lower())
    
    def test_comparison_output_formatting(self):
        """Test that output is properly formatted."""
        img1 = self.create_simple_image('format1.png')
        img2 = self.create_simple_image('format2.png')
        
        with patch('src.main.FaceComparator') as mock_comparator_class:
            mock_comparator = MagicMock()
            mock_comparator.compare_faces.return_value = (
                True, 
                {'confidence': 92.3, 'distance': 0.15}
            )
            mock_comparator_class.return_value = mock_comparator
            
            result = self.run_main_script([img1, img2])
            
            # Should include comparison header
            self.assertIn("Comparing", result.stdout)
            self.assertIn(os.path.basename(img1), result.stdout)
            self.assertIn(os.path.basename(img2), result.stdout)
            
            # Should include result with proper formatting
            self.assertIn("✅", result.stdout)
            self.assertIn("92.3", result.stdout)
    
    def test_missing_details_in_result(self):
        """Test handling when comparison result lacks expected details."""
        img1 = self.create_simple_image('missing1.png')
        img2 = self.create_simple_image('missing2.png')
        
        with patch('src.main.FaceComparator') as mock_comparator_class:
            mock_comparator = MagicMock()
            # Return result with missing keys
            mock_comparator.compare_faces.return_value = (True, {})
            mock_comparator_class.return_value = mock_comparator
            
            result = self.run_main_script([img1, img2])
            
            # Should handle missing keys gracefully
            self.assertEqual(result.returncode, 0)
            self.assertIn("SAME PERSON", result.stdout)
    
    def test_string_details_format(self):
        """Test handling when details is returned as string instead of dict."""
        img1 = self.create_simple_image('string1.png')
        img2 = self.create_simple_image('string2.png')
        
        with patch('src.main.FaceComparator') as mock_comparator_class:
            mock_comparator = MagicMock()
            # Return string details instead of dict
            mock_comparator.compare_faces.return_value = (False, "No faces detected")
            mock_comparator_class.return_value = mock_comparator
            
            result = self.run_main_script([img1, img2])
            
            # Should handle string details
            self.assertEqual(result.returncode, 0)
            self.assertIn("DIFFERENT PEOPLE", result.stdout)

class TestMainModuleDirectly(unittest.TestCase):
    """Test main.py by importing it directly."""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Add src to path for direct import
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        
    def tearDown(self):
        # Clean up sys.path
        sys.path = [p for p in sys.path if 'src' not in p or not p.endswith('src')]
    
    def test_main_function_with_mocked_argv(self):
        """Test main function by mocking sys.argv."""
        img1 = os.path.join(self.test_dir, 'mock1.png')
        img2 = os.path.join(self.test_dir, 'mock2.png')
        
        # Create simple test images
        Image.new('RGB', (50, 50), 'white').save(img1)
        Image.new('RGB', (50, 50), 'white').save(img2)
        
        with patch('sys.argv', ['main.py', img1, img2]):
            with patch('src.main.FaceComparator') as mock_comparator_class:
                mock_comparator = MagicMock()
                mock_comparator.compare_faces.return_value = (True, {'confidence': 88.8})
                mock_comparator_class.return_value = mock_comparator
                
                with patch('builtins.print') as mock_print:
                    import main
                    main.main()
                    
                    # Should have printed comparison result
                    print_calls = [str(call) for call in mock_print.call_args_list]
                    self.assertTrue(any('Comparing' in call for call in print_calls))
                    self.assertTrue(any('SAME PERSON' in call for call in print_calls))
    
    def test_import_and_function_existence(self):
        """Test that main module can be imported and has required functions."""
        try:
            import main
            self.assertTrue(hasattr(main, 'main'))
            self.assertTrue(callable(main.main))
        except ImportError as e:
            self.fail(f"Could not import main module: {e}")

def run_tests():
    """Run all extended main tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestMainScriptExtended))
    suite.addTests(loader.loadTestsFromTestCase(TestMainModuleDirectly))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Running extended tests for main script...")
    print("=" * 60)
    
    success = run_tests()
    
    if success:
        print("\n✅ All extended main tests passed!")
    else:
        print("\n❌ Some extended main tests failed!")
        exit(1)