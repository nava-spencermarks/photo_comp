#!/usr/bin/env python3
"""
Tests for image masking functionality.
"""

import json
import os
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Import after path modification  # noqa: E402
from src.image_masking import ImageMasker  # noqa: E402


class ImageMaskingTestCase(unittest.TestCase):
    """Test image masking functionality."""

    def setUp(self):
        """Set up test environment."""
        self.masker = ImageMasker()
        self.temp_dir = tempfile.mkdtemp()

        # Create test images
        self.test_image_path = os.path.join(self.temp_dir, "test_image.png")
        self.create_test_image(self.test_image_path, (200, 150))

        self.test_image_path2 = os.path.join(self.temp_dir, "test_image2.png")
        self.create_test_image(self.test_image_path2, (300, 200))

    def tearDown(self):
        """Clean up test environment."""
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def create_test_image(self, path: str, size: tuple):
        """Create a test image with gradient pattern."""
        width, height = size
        img = Image.new("RGB", (width, height))

        # Create simple gradient pattern for testing
        for y in range(height):
            for x in range(width):
                r = int((x / width) * 255)
                g = int((y / height) * 255)
                b = 128
                img.putpixel((x, y), (r, g, b))

        img.save(path)

    def test_parse_rectangle_data_valid(self):
        """Test parsing valid rectangle data."""
        rect_data = [
            {"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4},
            {"x": 0.5, "y": 0.6, "width": 0.2, "height": 0.1},
        ]

        json_str = json.dumps(rect_data)
        parsed = self.masker.parse_rectangle_data(json_str)

        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["x"], 0.1)
        self.assertEqual(parsed[0]["y"], 0.2)
        self.assertEqual(parsed[0]["width"], 0.3)
        self.assertEqual(parsed[0]["height"], 0.4)

    def test_parse_rectangle_data_empty(self):
        """Test parsing empty rectangle data."""
        parsed = self.masker.parse_rectangle_data("")
        self.assertEqual(len(parsed), 0)

        parsed = self.masker.parse_rectangle_data("[]")
        self.assertEqual(len(parsed), 0)

    def test_parse_rectangle_data_invalid(self):
        """Test parsing invalid rectangle data."""
        # Invalid JSON
        parsed = self.masker.parse_rectangle_data("invalid json")
        self.assertEqual(len(parsed), 0)

        # Missing required fields
        invalid_data = [{"x": 0.1, "y": 0.2}]  # Missing width, height
        json_str = json.dumps(invalid_data)
        parsed = self.masker.parse_rectangle_data(json_str)
        self.assertEqual(len(parsed), 0)

        # Out of bounds coordinates - should be clamped, not rejected
        invalid_data = [{"x": 0.8, "y": 0.2, "width": 0.3, "height": 0.4}]
 
        json_str = json.dumps(invalid_data)
        parsed = self.masker.parse_rectangle_data(json_str)
        # Should clamp width to fit within bounds
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["x"], 0.8)
        self.assertEqual(parsed[0]["y"], 0.2)
        self.assertAlmostEqual(
            parsed[0]["width"], 0.2, places=10
        )  # Clamped from 0.3 to 0.2
        self.assertEqual(parsed[0]["height"], 0.4)

        # Rectangle that would have no area after clamping
        invalid_data = [{"x": 1.0, "y": 1.0, "width": 0.3, "height": 0.4}]
        json_str = json.dumps(invalid_data)
        parsed = self.masker.parse_rectangle_data(json_str)
        self.assertEqual(len(parsed), 0)  # Should be rejected as it has no area

    def test_create_mask_from_rectangles_empty(self):
        """Test creating mask with no rectangles."""
        rectangles = []
        mask = self.masker.create_mask_from_rectangles(self.test_image_path, rectangles)

        # Should be all False (unmasked)
        self.assertEqual(mask.shape, (150, 200))  # height, width
        self.assertFalse(np.any(mask))

    def test_create_mask_from_rectangles_single(self):
        """Test creating mask with single rectangle."""
        rectangles = [{"x": 0.2, "y": 0.3, "width": 0.4, "height": 0.2}]
        mask = self.masker.create_mask_from_rectangles(self.test_image_path, rectangles)

        self.assertEqual(mask.shape, (150, 200))
        self.assertTrue(np.any(mask))  # Some pixels should be masked

        # Check specific region is masked
        # Rectangle should be at pixels (40, 45) to (120, 75)
        self.assertTrue(mask[50, 60])  # Should be masked
        self.assertFalse(mask[10, 10])  # Should be unmasked

    def test_create_mask_from_rectangles_multiple(self):
        """Test creating mask with multiple rectangles."""
        rectangles = [
            {"x": 0.1, "y": 0.1, "width": 0.2, "height": 0.2},
            {"x": 0.7, "y": 0.7, "width": 0.2, "height": 0.2},
        ]
        mask = self.masker.create_mask_from_rectangles(self.test_image_path, rectangles)

        self.assertEqual(mask.shape, (150, 200))
        self.assertTrue(np.any(mask))

        # Check both regions are masked
        self.assertTrue(mask[30, 40])  # First rectangle area
        self.assertTrue(mask[120, 160])  # Second rectangle area
        self.assertFalse(mask[75, 100])  # Between rectangles

    def test_apply_mask_to_image(self):
        """Test applying mask to image."""
        rectangles = [{"x": 0.0, "y": 0.0, "width": 0.5, "height": 0.5}]
        mask = self.masker.create_mask_from_rectangles(self.test_image_path, rectangles)

        masked_img = self.masker.apply_mask_to_image(self.test_image_path, mask)

        self.assertIsInstance(masked_img, Image.Image)
        self.assertEqual(masked_img.size, (200, 150))

        # Check that masked area is black
        masked_array = np.array(masked_img)
        self.assertTrue(
            np.all(masked_array[0, 0] == [0, 0, 0])
        )  # Top-left should be black

    def test_apply_mask_custom_color(self):
        """Test applying mask with custom color."""
        rectangles = [{"x": 0.0, "y": 0.0, "width": 0.5, "height": 0.5}]
        mask = self.masker.create_mask_from_rectangles(self.test_image_path, rectangles)

        red_color = (255, 0, 0)
        masked_img = self.masker.apply_mask_to_image(
            self.test_image_path, mask, red_color
        )

        # Check that masked area is red
        masked_array = np.array(masked_img)
        self.assertTrue(np.all(masked_array[0, 0] == [255, 0, 0]))

    def test_create_masked_image_file(self):
        """Test creating masked image file."""
        rectangles = [{"x": 0.25, "y": 0.25, "width": 0.5, "height": 0.5}]
        output_path = os.path.join(self.temp_dir, "masked_output.png")

        result_path = self.masker.create_masked_image_file(
            self.test_image_path, output_path, rectangles
        )

        self.assertEqual(result_path, output_path)
        self.assertTrue(os.path.exists(output_path))

        # Verify the created file is a valid image
        with Image.open(output_path) as img:
            self.assertEqual(img.size, (200, 150))

    def test_get_mask_statistics(self):
        """Test getting mask statistics."""
        # Create a known mask pattern
        mask = np.zeros((100, 100), dtype=bool)
        mask[25:75, 25:75] = True  # 50x50 masked area = 2500 pixels

        stats = self.masker.get_mask_statistics(mask)

        self.assertEqual(stats["total_pixels"], 10000)
        self.assertEqual(stats["masked_pixels"], 2500)
        self.assertEqual(stats["unmasked_pixels"], 7500)
        self.assertEqual(stats["mask_percentage"], 25.0)
        self.assertEqual(stats["unmasked_percentage"], 75.0)

    def test_validate_rectangles_match_identical(self):
        """Test validating identical rectangle sets."""
        rectangles1 = [
            {"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4},
            {"x": 0.5, "y": 0.6, "width": 0.2, "height": 0.1},
        ]
        rectangles2 = [
            {"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4},
            {"x": 0.5, "y": 0.6, "width": 0.2, "height": 0.1},
        ]

        self.assertTrue(self.masker.validate_rectangles_match(rectangles1, rectangles2))

    def test_validate_rectangles_match_within_tolerance(self):
        """Test validating rectangles within tolerance."""
        rectangles1 = [{"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4}]
        rectangles2 = [{"x": 0.101, "y": 0.199, "width": 0.301, "height": 0.399}]

        # Should match within tolerance
        self.assertTrue(
            self.masker.validate_rectangles_match(rectangles1, rectangles2, 0.01)
        )

        # Should not match with stricter tolerance
        self.assertFalse(
            self.masker.validate_rectangles_match(rectangles1, rectangles2, 0.001)
        )

    def test_validate_rectangles_match_different_length(self):
        """Test validating rectangle sets with different lengths."""
        rectangles1 = [{"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4}]
        rectangles2 = [
            {"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4},
            {"x": 0.5, "y": 0.6, "width": 0.2, "height": 0.1},
        ]

        self.assertFalse(
            self.masker.validate_rectangles_match(rectangles1, rectangles2)
        )

    def test_validate_rectangles_match_different_values(self):
        """Test validating rectangle sets with different values."""
        rectangles1 = [{"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4}]
        rectangles2 = [{"x": 0.2, "y": 0.2, "width": 0.3, "height": 0.4}]

        self.assertFalse(
            self.masker.validate_rectangles_match(rectangles1, rectangles2)
        )


def run_tests():
    """Run all image masking tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(ImageMaskingTestCase))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running image masking tests...")
    print("=" * 60)

    success = run_tests()

    if success:
        print("\n✅ All image masking tests passed!")
    else:
        print("\n❌ Some image masking tests failed!")
        exit(1)
