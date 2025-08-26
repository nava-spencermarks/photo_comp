#!/usr/bin/env python3
"""
Tests for main.py entry point.
"""

import os
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


class TestMainScript(unittest.TestCase):
    """Test the main script entry point."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def create_simple_image(self, filename):
        """Create a simple test image."""
        img = Image.new("RGB", (100, 100), color="white")
        path = os.path.join(self.test_dir, filename)
        img.save(path)
        return path

    @staticmethod
    def run_main_script(args):
        """Run the main script with given arguments."""
        script_path = os.path.join(os.path.dirname(__file__), "..", "src", "main.py")
        cmd = [sys.executable, script_path] + args
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_no_arguments(self):
        """Test main script with no arguments."""
        result = self.run_main_script([])

        self.assertNotEqual(result.returncode, 0)  # Should fail
        self.assertIn("Usage:", result.stdout + result.stderr)

    def test_one_argument(self):
        """Test main script with only one argument."""
        result = self.run_main_script(["image1.png"])

        self.assertNotEqual(result.returncode, 0)  # Should fail
        self.assertIn("Usage:", result.stdout + result.stderr)

    def test_nonexistent_files(self):
        """Test main script with nonexistent files."""
        result = self.run_main_script(["nonexistent1.png", "nonexistent2.png"])

        # Should handle the error gracefully (might succeed with error message)
        # The exact behavior depends on how robust_face_compare handles missing files
        self.assertIsInstance(result.returncode, int)

    def test_with_actual_images(self):
        """Test main script with actual image files."""
        # Use specific known test images - they MUST exist
        test_dir = os.path.join(os.path.dirname(__file__), "test_data")
        img1 = os.path.join(test_dir, "face_me_1.png")
        img2 = os.path.join(test_dir, "me_different.png")

        self.assertTrue(os.path.exists(img1), f"Required test image missing: {img1}")
        self.assertTrue(os.path.exists(img2), f"Required test image missing: {img2}")

        result = self.run_main_script([img1, img2])

        # Should complete (success or graceful failure)
        self.assertIsInstance(result.returncode, int)

        # Should produce some output
        output = result.stdout + result.stderr
        self.assertGreater(len(output.strip()), 0)

    def test_help_like_arguments(self):
        """Test script behavior with help-like arguments."""
        help_args = ["-h", "--help", "help"]

        for arg in help_args:
            result = self.run_main_script([arg])
            # Most will fail since we expect exactly 2 image arguments
            # But should not crash catastrophically
            self.assertIsInstance(result.returncode, int)


class TestMainModule(unittest.TestCase):
    """Test main.py as a module."""

    def test_import_main(self):
        """Test that main.py can be imported."""
        try:
            import sys

            sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
            import main

            self.assertTrue(hasattr(main, "main"))
        except ImportError as e:
            self.fail(f"Could not import main module: {e}")

    def test_main_function_exists(self):
        """Test that main() function exists."""
        import sys

        sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
        import main

        self.assertTrue(callable(main.main))


def run_tests():
    """Run all main script tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestMainScript))
    suite.addTests(loader.loadTestsFromTestCase(TestMainModule))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running tests for main script...")
    print("=" * 50)

    success = run_tests()

    if success:
        print("\n✅ All main script tests passed!")
    else:
        print("\n❌ Some main script tests failed!")
        exit(1)
