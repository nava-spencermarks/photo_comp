#!/usr/bin/env python3
"""
Tests for rectangle drawing frontend functionality.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Import after path modification  # noqa: E402
from app import app


class RectangleFrontendTestCase(unittest.TestCase):
    """Test rectangle drawing functionality in the frontend."""

    def setUp(self):
        """Set up test environment."""
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["UPLOAD_FOLDER"] = tempfile.mkdtemp()

        # Create test upload directory
        Path(self.app.config["UPLOAD_FOLDER"]).mkdir(exist_ok=True)

    def tearDown(self):
        """Clean up test environment."""
        import shutil

        if os.path.exists(self.app.config["UPLOAD_FOLDER"]):
            shutil.rmtree(self.app.config["UPLOAD_FOLDER"])

    def test_rectangle_javascript_classes_present(self):
        """Test that rectangle drawing JavaScript classes are present."""
        # This is a basic test to verify the JavaScript structure
        # In a real scenario, we'd use a JavaScript testing framework

        # Read the index template to verify JavaScript is present
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", "index.html"
        )

        with open(template_path, "r") as f:
            content = f.read()

        # Verify key JavaScript components are present
        self.assertIn("class RectangleDrawer", content)
        self.assertIn("handleMouseDown", content)
        self.assertIn("handleMouseMove", content)
        self.assertIn("handleMouseUp", content)
        self.assertIn("syncRectangles", content)
        self.assertIn("clearRectangles", content)
        self.assertIn("toggleDrawMode", content)

    def test_canvas_elements_present_in_template(self):
        """Test that canvas elements are present in the template."""
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", "index.html"
        )

        with open(template_path, "r") as f:
            content = f.read()

        # Verify canvas elements are present
        self.assertIn('<canvas id="canvas1"', content)
        self.assertIn('<canvas id="canvas2"', content)
        self.assertIn("canvas-container-1", content)
        self.assertIn("canvas-container-2", content)
        self.assertIn("Clear All", content)
        self.assertIn("Draw Mode", content)

    def test_css_classes_present_in_base_template(self):
        """Test that CSS classes for canvas controls are present."""
        base_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", "base.html"
        )

        with open(base_path, "r") as f:
            content = f.read()

        # Verify CSS classes are present
        self.assertIn(".canvas-controls", content)
        self.assertIn(".btn-small", content)
        self.assertIn(".image-canvas-container", content)

    def test_form_submission_rectangle_data(self):
        """Test that rectangle data is added to form submission."""
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", "index.html"
        )

        with open(template_path, "r") as f:
            content = f.read()

        # Verify form submission code is present
        self.assertIn("addEventListener('submit'", content)
        self.assertIn("getRectangleData", content)
        self.assertIn("rectangles1", content)
        self.assertIn("rectangles2", content)
        self.assertIn("JSON.stringify", content)


class RectangleDrawerUnitTests(unittest.TestCase):
    """Unit tests for rectangle drawing logic."""

    def test_rectangle_drawer_methods_defined(self):
        """Test that all required methods are defined in JavaScript."""
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", "index.html"
        )

        with open(template_path, "r") as f:
            content = f.read()

        required_methods = [
            "setupEventListeners",
            "updateCanvasSize",
            "getMousePos",
            "handleMouseDown",
            "handleMouseMove",
            "handleMouseUp",
            "findRectangleAt",
            "redraw",
            "clearRectangles",
            "toggleDrawMode",
            "syncRectangles",
            "getRectangleData",
        ]

        for method in required_methods:
            self.assertIn(method, content, f"Method {method} not found in JavaScript")

    def test_rectangle_synchronization_logic(self):
        """Test that rectangle synchronization logic is present."""
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", "index.html"
        )

        with open(template_path, "r") as f:
            content = f.read()

        # Verify sync logic components
        self.assertIn("syncRectangles", content)
        self.assertIn("syncDrawingPreview", content)
        self.assertIn("otherDrawer", content)
        self.assertIn("canvas1_drawer", content)
        self.assertIn("canvas2_drawer", content)

    def test_rectangle_data_structure(self):
        """Test that rectangle data structure is properly normalized."""
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", "index.html"
        )

        with open(template_path, "r") as f:
            content = f.read()

        # Verify normalization logic (converting to relative coordinates)
        self.assertIn("canvas.width", content)
        self.assertIn("canvas.height", content)
        self.assertIn("getRectangleData", content)

    def test_event_handling_structure(self):
        """Test that event handling is properly structured."""
        template_path = os.path.join(
            os.path.dirname(__file__), "..", "templates", "index.html"
        )

        with open(template_path, "r") as f:
            content = f.read()

        # Verify event handling
        self.assertIn("addEventListener", content)
        self.assertIn("mousedown", content)
        self.assertIn("mousemove", content)
        self.assertIn("mouseup", content)


def run_tests():
    """Run all rectangle frontend tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(RectangleFrontendTestCase))
    suite.addTests(loader.loadTestsFromTestCase(RectangleDrawerUnitTests))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running rectangle frontend tests...")
    print("=" * 60)

    success = run_tests()

    if success:
        print("\n✅ All rectangle frontend tests passed!")
    else:
        print("\n❌ Some rectangle frontend tests failed!")
        exit(1)
