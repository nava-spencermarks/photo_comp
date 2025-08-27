#!/usr/bin/env python3
"""
Tests for the Flask web application.
"""

import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Import after path modification  # noqa: E402
from app import app


class WebAppTestCase(unittest.TestCase):
    """Test the Flask web application."""

    def setUp(self):
        """Set up test environment."""
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["UPLOAD_FOLDER"] = tempfile.mkdtemp()
        self.client = self.app.test_client()

        # Create test upload directory
        Path(self.app.config["UPLOAD_FOLDER"]).mkdir(exist_ok=True)

    def tearDown(self):
        """Clean up test environment."""
        import shutil

        if os.path.exists(self.app.config["UPLOAD_FOLDER"]):
            shutil.rmtree(self.app.config["UPLOAD_FOLDER"])

    def create_test_image(self):
        """Create a simple test image file."""
        from PIL import Image

        img = Image.new("RGB", (100, 100), color="white")
        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        return img_io

    def test_index_page_loads(self):
        """Test that the index page loads successfully."""
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Face Comparison App", response.data)
        self.assertIn(b"Upload two images", response.data)
        self.assertIn(b"Choose first image", response.data)
        self.assertIn(b"Choose second image", response.data)

    def test_index_page_has_form(self):
        """Test that the index page contains the upload form."""
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<form", response.data)
        self.assertIn(b'enctype="multipart/form-data"', response.data)
        self.assertIn(b'name="image1"', response.data)
        self.assertIn(b'name="image2"', response.data)
        self.assertIn(b"Compare Faces", response.data)

    def test_compare_no_files(self):
        """Test compare endpoint with no files uploaded."""
        response = self.client.post("/compare")

        # Should redirect back to index with flash message
        self.assertEqual(response.status_code, 302)
        self.assertIn("/", response.location)

    def test_compare_missing_files(self):
        """Test compare endpoint with missing files."""
        # Only send one file
        data = {"image1": (io.BytesIO(b"fake image"), "test1.png")}
        response = self.client.post("/compare", data=data)

        # Should redirect back to index
        self.assertEqual(response.status_code, 302)

    def test_compare_empty_filenames(self):
        """Test compare endpoint with empty filenames."""
        data = {"image1": (io.BytesIO(b""), ""), "image2": (io.BytesIO(b""), "")}
        response = self.client.post("/compare", data=data)

        # Should redirect back to index
        self.assertEqual(response.status_code, 302)

    def test_compare_invalid_file_types(self):
        """Test compare endpoint with invalid file types."""
        data = {
            "image1": (io.BytesIO(b"fake content"), "test.txt"),
            "image2": (io.BytesIO(b"fake content"), "test.doc"),
        }
        response = self.client.post("/compare", data=data)

        # Should redirect back to index
        self.assertEqual(response.status_code, 302)

    @patch("app.FaceComparator")
    def test_compare_valid_images_success(self, mock_comparator_class):
        """Test compare endpoint with valid images that match."""
        # Mock the face comparator
        mock_comparator = MagicMock()
        mock_comparator.compare_faces.return_value = (
            True,
            "Distance: 0.123, Confidence: 95.5%",
        )
        mock_comparator_class.return_value = mock_comparator

        # Create test images
        img1 = self.create_test_image()
        img2 = self.create_test_image()

        data = {"image1": (img1, "test1.png"), "image2": (img2, "test2.png")}

        response = self.client.post("/compare", data=data, follow_redirects=True)

        # Should show results page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Comparison Results", response.data)
        self.assertIn(b"SAME PERSON", response.data)
        self.assertIn(b"test1.png", response.data)
        self.assertIn(b"test2.png", response.data)

    @patch("app.FaceComparator")
    def test_compare_valid_images_different(self, mock_comparator_class):
        """Test compare endpoint with valid images that don't match."""
        # Mock the face comparator
        mock_comparator = MagicMock()
        mock_comparator.compare_faces.return_value = (
            False,
            "Distance: 0.789, Confidence: 85.2%",
        )
        mock_comparator_class.return_value = mock_comparator

        # Create test images
        img1 = self.create_test_image()
        img2 = self.create_test_image()

        data = {"image1": (img1, "person1.jpg"), "image2": (img2, "person2.jpg")}

        response = self.client.post("/compare", data=data, follow_redirects=True)

        # Should show results page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Comparison Results", response.data)
        self.assertIn(b"DIFFERENT PEOPLE", response.data)
        self.assertIn(b"person1.jpg", response.data)
        self.assertIn(b"person2.jpg", response.data)

    @patch("app.FaceComparator")
    def test_compare_face_comparison_error(self, mock_comparator_class):
        """Test compare endpoint when face comparison throws an error."""
        # Mock the face comparator to throw an exception
        mock_comparator = MagicMock()
        mock_comparator.compare_faces.side_effect = Exception("Face detection failed")
        mock_comparator_class.return_value = mock_comparator

        # Create test images
        img1 = self.create_test_image()
        img2 = self.create_test_image()

        data = {"image1": (img1, "error1.png"), "image2": (img2, "error2.png")}

        response = self.client.post("/compare", data=data)

        # Should redirect back to index
        self.assertEqual(response.status_code, 302)

    def test_file_extension_validation(self):
        """Test the allowed_file function."""
        from app import allowed_file

        # Valid extensions
        self.assertTrue(allowed_file("test.png"))
        self.assertTrue(allowed_file("test.jpg"))
        self.assertTrue(allowed_file("test.jpeg"))
        self.assertTrue(allowed_file("test.gif"))
        self.assertTrue(allowed_file("test.bmp"))
        self.assertTrue(allowed_file("TEST.PNG"))  # Case insensitive

        # Invalid extensions
        self.assertFalse(allowed_file("test.txt"))
        self.assertFalse(allowed_file("test.doc"))
        self.assertFalse(allowed_file("test.pdf"))
        self.assertFalse(allowed_file("test"))  # No extension
        self.assertFalse(allowed_file(".png"))  # No filename

    def test_uploaded_file_endpoint(self):
        """Test the uploaded file serving endpoint."""
        # Create a test file in upload directory
        test_file_path = os.path.join(self.app.config["UPLOAD_FOLDER"], "test.png")
        with open(test_file_path, "wb") as f:
            f.write(b"fake image data")

        response = self.client.get("/uploads/test.png")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"fake image data")

    def test_uploaded_file_not_found(self):
        """Test the uploaded file endpoint with non-existent file."""
        response = self.client.get("/uploads/nonexistent.png")

        self.assertEqual(response.status_code, 404)

    def test_flash_messages_display(self):
        """Test that flash messages are displayed correctly."""
        with self.client.session_transaction() as sess:
            sess["_flashes"] = [("message", "Test flash message")]

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test flash message", response.data)
        self.assertIn(b"flash-message", response.data)

    @patch("app.FaceComparator")
    def test_compare_with_rectangle_data(self, mock_comparator_class):
        """Test compare endpoint with rectangle masking data."""
        # Mock the face comparator
        mock_comparator = MagicMock()
        mock_comparator.compare_faces.return_value = (
            True,
            "Distance: 0.234, Confidence: 92.1%",
        )
        mock_comparator_class.return_value = mock_comparator

        # Create test images
        img1 = self.create_test_image()
        img2 = self.create_test_image()

        # Rectangle data (normalized coordinates)
        rectangles = [{"x": 0.2, "y": 0.3, "width": 0.4, "height": 0.2}]

        data = {
            "image1": (img1, "test1.png"),
            "image2": (img2, "test2.png"),
            "rectangles1": json.dumps(rectangles),
            "rectangles2": json.dumps(rectangles),
        }

        response = self.client.post("/compare", data=data, follow_redirects=True)

        # Should show results page with masking info
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Comparison Results", response.data)
        self.assertIn(b"Masked Comparison Applied", response.data)
        self.assertIn(b"Rectangles used: 1", response.data)

    @patch("app.FaceComparator")
    def test_compare_without_rectangle_data(self, mock_comparator_class):
        """Test compare endpoint without rectangle masking."""
        # Mock the face comparator
        mock_comparator = MagicMock()
        mock_comparator.compare_faces.return_value = (
            False,
            "Distance: 0.789, Confidence: 88.3%",
        )
        mock_comparator_class.return_value = mock_comparator

        # Create test images
        img1 = self.create_test_image()
        img2 = self.create_test_image()

        data = {
            "image1": (img1, "test1.png"),
            "image2": (img2, "test2.png"),
            # No rectangle data
        }

        response = self.client.post("/compare", data=data, follow_redirects=True)

        # Should show results page without masking info
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Comparison Results", response.data)
        self.assertNotIn(b"Masked Comparison Applied", response.data)
        self.assertIn(b"Full image analysis", response.data)

    @patch("app.ImageMasker")
    @patch("app.FaceComparator")
    def test_compare_with_masking_error(self, mock_comparator_class, mock_masker_class):
        """Test compare endpoint when masking fails."""
        # Mock the masker to throw an exception
        mock_masker = MagicMock()
        mock_masker.parse_rectangle_data.side_effect = Exception("Masking failed")
        mock_masker_class.return_value = mock_masker

        # Create test images
        img1 = self.create_test_image()
        img2 = self.create_test_image()

        data = {
            "image1": (img1, "error1.png"),
            "image2": (img2, "error2.png"),
            "rectangles1": '[{"x": 0.1, "y": 0.1, "width": 0.2, "height": 0.2}]',
        }

        response = self.client.post("/compare", data=data)

        # Should redirect back to index with error
        self.assertEqual(response.status_code, 302)

    def test_rectangle_data_validation(self):
        """Test that rectangle data is properly validated."""
        from src.image_masking import ImageMasker
        
        masker = ImageMasker()
        
        # Valid rectangle data
        valid_json = '[{"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4}]'
        rectangles = masker.parse_rectangle_data(valid_json)
        self.assertEqual(len(rectangles), 1)
        
        # Invalid rectangle data
        invalid_json = '[{"x": 1.5, "y": 0.2}]'  # x out of bounds, missing fields
        rectangles = masker.parse_rectangle_data(invalid_json)
        self.assertEqual(len(rectangles), 0)


class WebAppIntegrationTestCase(unittest.TestCase):
    """Integration tests for the web application."""

    def setUp(self):
        """Set up test environment."""
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["UPLOAD_FOLDER"] = tempfile.mkdtemp()
        self.client = self.app.test_client()

        # Create test upload directory
        Path(self.app.config["UPLOAD_FOLDER"]).mkdir(exist_ok=True)

    def tearDown(self):
        """Clean up test environment."""
        import shutil

        if os.path.exists(self.app.config["UPLOAD_FOLDER"]):
            shutil.rmtree(self.app.config["UPLOAD_FOLDER"])

    def test_full_workflow_with_real_face_comparator(self):
        """Test the full workflow with the actual face comparator."""
        # Skip this test if test images don't exist
        test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")
        test_img1 = os.path.join(test_data_dir, "face_me_1.png")

        if not os.path.exists(test_img1):
            self.skipTest("Test images not available")

        # Read test images
        with open(test_img1, "rb") as f:
            img1_data = f.read()

        # Use the same image twice (should match)
        data = {
            "image1": (io.BytesIO(img1_data), "face1.png"),
            "image2": (io.BytesIO(img1_data), "face2.png"),
        }

        response = self.client.post("/compare", data=data, follow_redirects=True)

        # Should complete successfully (may or may not match depending on face detection)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Comparison Results", response.data)


def run_tests():
    """Run all web app tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(WebAppTestCase))
    suite.addTests(loader.loadTestsFromTestCase(WebAppIntegrationTestCase))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running web app tests...")
    print("=" * 60)

    success = run_tests()

    if success:
        print("\n✅ All web app tests passed!")
    else:
        print("\n❌ Some web app tests failed!")
        exit(1)
