#!/usr/bin/env python3
"""
Tests for the image inspection utility.
"""

import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# Import after path modification  # noqa: E402
import inspect_image


class TestInspectImage(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def create_test_image(
        self, filename, width=200, height=200, mode="RGB", brightness=128
    ):
        """Create a test image for testing."""
        if mode == "RGB":
            color = (brightness, brightness, brightness)
        else:
            color = brightness

        image = Image.new(mode, (width, height), color=color)
        filepath = os.path.join(self.test_dir, filename)
        image.save(filepath)
        return filepath

    @patch("builtins.print")
    def test_inspect_nonexistent_file(self, mock_print):
        """Test inspect_image with nonexistent file."""
        fake_path = os.path.join(self.test_dir, "nonexistent.png")
        inspect_image.inspect_image(fake_path)

        # Should print error message
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("File does not exist" in call for call in calls))

    @patch("builtins.print")
    def test_inspect_normal_image(self, mock_print):
        """Test inspect_image with normal image."""
        img_path = self.create_test_image("normal.png", 400, 300)
        inspect_image.inspect_image(img_path)

        # Should print various image details
        calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join(calls)  # noqa: F841

        self.assertTrue(any("INSPECTING" in call for call in calls))
        self.assertTrue(any("Image dimensions" in call for call in calls))
        self.assertTrue(any("bytes" in call for call in calls))

    @patch("builtins.print")
    def test_inspect_large_image(self, mock_print):
        """Test inspect_image with very large image."""
        img_path = self.create_test_image("large.png", 4000, 3000)
        inspect_image.inspect_image(img_path)

        calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join(calls)  # noqa: F841

        # Should warn about large image
        self.assertTrue(any("very large" in call.lower() for call in calls))

    @patch("builtins.print")
    def test_inspect_dark_image(self, mock_print):
        """Test inspect_image with very dark image."""
        img_path = self.create_test_image("dark.png", brightness=20)
        inspect_image.inspect_image(img_path)

        calls = [str(call) for call in mock_print.call_args_list]

        # Should warn about darkness
        self.assertTrue(any("very dark" in call.lower() for call in calls))

    @patch("builtins.print")
    def test_inspect_bright_image(self, mock_print):
        """Test inspect_image with very bright image."""
        img_path = self.create_test_image("bright.png", brightness=220)
        inspect_image.inspect_image(img_path)

        calls = [str(call) for call in mock_print.call_args_list]

        # Should warn about brightness
        self.assertTrue(any("very bright" in call.lower() for call in calls))

    @patch("builtins.print")
    def test_inspect_low_contrast_image(self, mock_print):
        """Test inspect_image with low contrast image."""
        # Create an image with very uniform color (low contrast)
        img_path = self.create_test_image("low_contrast.png", brightness=128)
        inspect_image.inspect_image(img_path)

        calls = [str(call) for call in mock_print.call_args_list]

        # Should detect low contrast
        self.assertTrue(any("contrast" in call.lower() for call in calls))

    @patch("builtins.print")
    @patch("face_recognition.load_image_file")
    def test_inspect_image_load_error(self, mock_load, mock_print):
        """Test inspect_image when face_recognition fails to load."""
        img_path = self.create_test_image("error.png")
        mock_load.side_effect = Exception("Load error")

        inspect_image.inspect_image(img_path)

        calls = [str(call) for call in mock_print.call_args_list]

        # Should handle error gracefully
        self.assertTrue(any("Error loading" in call for call in calls))

    @patch("builtins.print")
    @patch("os.listdir")
    def test_main_function(self, mock_listdir, mock_print):
        """Test main function that processes directory."""
        # Mock directory listing
        mock_listdir.return_value = ["test1.png", "test2.jpg", "not_image.txt"]

        # Mock the inspect_image function to avoid actual processing
        with patch("inspect_image.inspect_image") as mock_inspect:
            with patch("os.path.exists", return_value=True):
                inspect_image.main()

                # Should have called inspect_image for image files only
                self.assertEqual(mock_inspect.call_count, 2)

                # Should have called with image files
                called_files = [call[0][0] for call in mock_inspect.call_args_list]
                self.assertIn("test1.png", called_files)
                self.assertIn("test2.jpg", called_files)
                self.assertNotIn("not_image.txt", called_files)


class TestInspectImageIntegration(unittest.TestCase):
    """Integration tests with real image processing."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_realistic_test_image(self, filename):
        """Create a more realistic test image with some variation."""
        # Create image with gradient for more realistic contrast
        width, height = 200, 200
        image = Image.new("RGB", (width, height))
        pixels = []

        for y in range(height):
            for x in range(width):
                # Create gradient with some noise
                gray_val = int(128 + 50 * np.sin(x / 20) * np.cos(y / 20))
                gray_val = max(0, min(255, gray_val))
                pixels.append((gray_val, gray_val, gray_val))

        image.putdata(pixels)
        filepath = os.path.join(self.test_dir, filename)
        image.save(filepath)
        return filepath

    @patch("builtins.print")
    def test_realistic_image_inspection(self, mock_print):
        """Test with realistic image that has actual contrast."""
        img_path = self.create_realistic_test_image("realistic.png")

        # Should not raise any exceptions
        inspect_image.inspect_image(img_path)

        # Should have printed inspection results
        self.assertTrue(mock_print.called)
        calls = [str(call) for call in mock_print.call_args_list]

        # Should include various analysis sections
        self.assertTrue(any("INSPECTING" in call for call in calls))
        self.assertTrue(any("OpenCV Detection" in call for call in calls))
        self.assertTrue(any("Face_recognition Tests" in call for call in calls))


def run_tests():
    """Run all inspect_image tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestInspectImage))
    suite.addTests(loader.loadTestsFromTestCase(TestInspectImageIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running tests for inspect_image...")
    print("=" * 50)

    success = run_tests()

    if success:
        print("\n✅ All inspect_image tests passed!")
    else:
        print("\n❌ Some inspect_image tests failed!")
        exit(1)
