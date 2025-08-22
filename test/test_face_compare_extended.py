#!/usr/bin/env python3
"""
Extended tests for face comparison to increase code coverage.
"""

import unittest
import os
import sys
import tempfile
import shutil
from PIL import Image, ImageDraw
import numpy as np
from unittest.mock import patch, MagicMock, call
import cv2

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from face_compare import FaceComparator

class TestFaceComparatorExtended(unittest.TestCase):
    """Extended tests to cover more code paths."""
    
    def setUp(self):
        """Set up test environment."""
        self.comparator = FaceComparator()
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def create_test_image(self, filename, width=200, height=200, has_face_pattern=False):
        """Create a test image for testing."""
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        if has_face_pattern:
            # Draw a simple face-like pattern
            center_x, center_y = width // 2, height // 2
            face_radius = min(width, height) // 4
            
            # Face outline
            draw.ellipse([center_x - face_radius, center_y - face_radius, 
                         center_x + face_radius, center_y + face_radius], 
                        outline='black', width=2)
            
            # Eyes
            eye_offset = face_radius // 3
            eye_radius = face_radius // 8
            draw.ellipse([center_x - eye_offset - eye_radius, center_y - eye_offset - eye_radius,
                         center_x - eye_offset + eye_radius, center_y - eye_offset + eye_radius], 
                        fill='black')
            draw.ellipse([center_x + eye_offset - eye_radius, center_y - eye_offset - eye_radius,
                         center_x + eye_offset + eye_radius, center_y - eye_offset + eye_radius], 
                        fill='black')
        
        filepath = os.path.join(self.test_dir, filename)
        image.save(filepath)
        return filepath
    
    def test_constructor_with_custom_tolerance(self):
        """Test FaceComparator constructor with custom tolerance."""
        custom_comparator = FaceComparator(tolerance=0.3)
        self.assertEqual(custom_comparator.tolerance, 0.3)
        
        default_comparator = FaceComparator()
        self.assertEqual(default_comparator.tolerance, 0.45)
    
    def test_preprocess_image_variations_different_sizes(self):
        """Test preprocessing with different image sizes."""
        # Test with very small image
        small_img = self.create_test_image('small.png', 50, 50)
        variations = self.comparator.preprocess_image_variations(small_img)
        self.assertGreater(len(variations), 0)
        
        # Test with very large image
        large_img = self.create_test_image('large.png', 2000, 1500)
        variations = self.comparator.preprocess_image_variations(large_img)
        self.assertGreater(len(variations), 0)
        
        # Each variation should have proper structure
        for name, img_array in variations:
            self.assertIsInstance(name, str)
            self.assertIsInstance(img_array, np.ndarray)
    
    @patch('face_recognition.load_image_file')
    def test_preprocess_image_variations_load_error(self, mock_load):
        """Test preprocessing when image load fails."""
        mock_load.side_effect = Exception("Load failed")
        
        fake_path = os.path.join(self.test_dir, 'fake.png')
        variations = self.comparator.preprocess_image_variations(fake_path)
        
        # Should return empty list on error
        self.assertEqual(len(variations), 0)
    
    def test_detect_with_opencv_fallback_different_settings(self):
        """Test OpenCV fallback with different detection scenarios."""
        # Create test image with face-like pattern
        img_path = self.create_test_image('opencv_test.png', 200, 200, has_face_pattern=True)
        test_img = Image.open(img_path)
        img_np = np.array(test_img)
        
        # Test OpenCV detection (may or may not find faces, but shouldn't crash)
        faces = self.comparator.detect_with_opencv_fallback(img_np)
        self.assertIsInstance(faces, list)
        
        # Each detected face should be a tuple of 4 coordinates
        for face in faces:
            self.assertEqual(len(face), 4)
            self.assertTrue(all(isinstance(coord, (int, np.integer)) for coord in face))
    
    @patch('cv2.CascadeClassifier')
    def test_opencv_fallback_cascade_error(self, mock_cascade_class):
        """Test OpenCV fallback when cascade classifier fails."""
        mock_cascade = MagicMock()
        mock_cascade.detectMultiScale.side_effect = Exception("Cascade error")
        mock_cascade_class.return_value = mock_cascade
        
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        faces = self.comparator.detect_with_opencv_fallback(img)
        
        # Should return empty list on error
        self.assertEqual(faces, [])
    
    def test_get_face_encodings_strategies(self):
        """Test get_face_encodings with different detection strategies."""
        img_path = self.create_test_image('strategies_test.png', 300, 300, has_face_pattern=True)
        
        # Test that it tries different strategies (mock to control behavior)
        with patch('face_recognition.face_locations') as mock_locations:
            with patch('face_recognition.face_encodings') as mock_encodings:
                # First strategy fails, second succeeds
                mock_locations.side_effect = [[], [(10, 50, 40, 20)]]  # No faces, then 1 face
                mock_encodings.return_value = [np.array([0.1, 0.2, 0.3])]
                
                encodings, message = self.comparator.get_face_encodings(img_path)
                
                # Should have tried multiple strategies
                self.assertGreaterEqual(mock_locations.call_count, 2)
                self.assertIsNotNone(encodings)
    
    @patch('face_recognition.face_locations')
    @patch('face_recognition.load_image_file')
    def test_get_face_encodings_all_strategies_fail(self, mock_load, mock_locations):
        """Test when all detection strategies fail."""
        mock_load.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_locations.return_value = []  # No faces detected by any strategy
        
        img_path = self.create_test_image('no_faces.png')
        encodings, message = self.comparator.get_face_encodings(img_path)
        
        self.assertIsNone(encodings)
        self.assertIn("No faces detected", message)
    
    @patch('face_recognition.face_encodings')
    def test_get_face_encodings_encoding_error(self, mock_encodings):
        """Test when face encoding fails."""
        mock_encodings.side_effect = Exception("Encoding failed")
        
        with patch('face_recognition.face_locations', return_value=[(10, 50, 40, 20)]):
            img_path = self.create_test_image('encoding_error.png')
            encodings, message = self.comparator.get_face_encodings(img_path)
            
            self.assertIsNone(encodings)
            self.assertIn("Error during encoding", message)
    
    def test_compare_faces_comprehensive_scenarios(self):
        """Test compare_faces with various scenarios."""
        img1_path = self.create_test_image('comp1.png')
        img2_path = self.create_test_image('comp2.png')
        
        # Test when one image has no faces
        with patch.object(self.comparator, 'get_face_encodings') as mock_encodings:
            # First image has no faces, second has faces
            mock_encodings.side_effect = [
                (None, "No faces detected in first image"),
                ([np.array([0.1, 0.2])], "1 face found")
            ]
            
            is_same, details = self.comparator.compare_faces(img1_path, img2_path)
            self.assertFalse(is_same)
            self.assertIsInstance(details, str)
            self.assertIn("faces", details.lower())
    
    def test_compare_faces_distance_calculation(self):
        """Test distance calculation in compare_faces."""
        img1_path = self.create_test_image('dist1.png')
        img2_path = self.create_test_image('dist2.png')
        
        with patch.object(self.comparator, 'get_face_encodings') as mock_encodings:
            # Mock similar faces (low distance)
            encoding1 = np.array([0.1, 0.2, 0.3, 0.4])
            encoding2 = np.array([0.1, 0.2, 0.3, 0.4])  # Very similar
            
            mock_encodings.side_effect = [
                ([encoding1], "1 face found"),
                ([encoding2], "1 face found")
            ]
            
            is_same, details = self.comparator.compare_faces(img1_path, img2_path)
            self.assertTrue(is_same)
            self.assertIsInstance(details, str)
            self.assertIn("SAME", details.upper())
    
    def test_compare_faces_multiple_faces_matching(self):
        """Test compare_faces when images have multiple faces."""
        img1_path = self.create_test_image('multi1.png')
        img2_path = self.create_test_image('multi2.png')
        
        with patch.object(self.comparator, 'get_face_encodings') as mock_encodings:
            # Multiple faces in each image
            encoding1a = np.array([0.1, 0.2, 0.3])
            encoding1b = np.array([0.7, 0.8, 0.9])
            encoding2a = np.array([0.1, 0.2, 0.3])  # Matches encoding1a
            encoding2b = np.array([0.4, 0.5, 0.6])
            
            mock_encodings.side_effect = [
                ([encoding1a, encoding1b], "2 faces found"),
                ([encoding2a, encoding2b], "2 faces found")
            ]
            
            is_same, details = self.comparator.compare_faces(img1_path, img2_path)
            # Should find matching faces
            self.assertIsInstance(details, str)
            self.assertIn("face", details.lower())
    
    @patch('face_recognition.load_image_file')
    def test_compare_faces_file_error(self, mock_load):
        """Test compare_faces when file loading fails."""
        mock_load.side_effect = Exception("File not found")
        
        img1_path = os.path.join(self.test_dir, 'nonexistent1.png')
        img2_path = os.path.join(self.test_dir, 'nonexistent2.png')
        
        is_same, details = self.comparator.compare_faces(img1_path, img2_path)
        self.assertFalse(is_same)
        self.assertIsInstance(details, str)
    
    def test_edge_cases_and_error_handling(self):
        """Test various edge cases and error conditions."""
        # Test with very different encodings (high distance)
        with patch.object(self.comparator, 'get_face_encodings') as mock_encodings:
            encoding1 = np.array([0.0, 0.0, 0.0, 0.0])
            encoding2 = np.array([1.0, 1.0, 1.0, 1.0])  # Very different
            
            mock_encodings.side_effect = [
                ([encoding1], "1 face found"),
                ([encoding2], "1 face found")
            ]
            
            img1_path = self.create_test_image('different1.png')
            img2_path = self.create_test_image('different2.png')
            
            is_same, details = self.comparator.compare_faces(img1_path, img2_path)
            self.assertFalse(is_same)
            self.assertIsInstance(details, str)
            self.assertIn("DIFFERENT", details.upper())

class TestFaceComparatorErrorCoverage(unittest.TestCase):
    """Tests specifically for error handling and edge cases."""
    
    def setUp(self):
        self.comparator = FaceComparator()
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_malformed_image_handling(self):
        """Test handling of malformed or corrupted image files."""
        # Create a file that looks like an image but isn't
        fake_img_path = os.path.join(self.test_dir, 'fake.png')
        with open(fake_img_path, 'w') as f:
            f.write("This is not an image file")
        
        encodings, message = self.comparator.get_face_encodings(fake_img_path)
        self.assertIsNone(encodings)
        self.assertIsInstance(message, str)
    
    @patch('face_recognition.face_distance')
    def test_distance_calculation_error(self, mock_distance):
        """Test when face distance calculation fails."""
        mock_distance.side_effect = Exception("Distance calculation failed")
        
        img1_path = os.path.join(self.test_dir, 'dist_err1.png')
        img2_path = os.path.join(self.test_dir, 'dist_err2.png')
        
        # Create minimal images
        Image.new('RGB', (10, 10), 'white').save(img1_path)
        Image.new('RGB', (10, 10), 'white').save(img2_path)
        
        with patch.object(self.comparator, 'get_face_encodings') as mock_encodings:
            mock_encodings.side_effect = [
                ([np.array([0.1, 0.2])], "1 face found"),
                ([np.array([0.3, 0.4])], "1 face found")
            ]
            
            is_same, details = self.comparator.compare_faces(img1_path, img2_path)
            self.assertFalse(is_same)
            self.assertIsInstance(details, str)
            # Should handle the error gracefully

def run_tests():
    """Run all extended face comparison tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestFaceComparatorExtended))
    suite.addTests(loader.loadTestsFromTestCase(TestFaceComparatorErrorCoverage))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Running extended tests for face comparison...")
    print("=" * 60)
    
    success = run_tests()
    
    if success:
        print("\n✅ All extended face comparison tests passed!")
    else:
        print("\n❌ Some extended face comparison tests failed!")
        exit(1)