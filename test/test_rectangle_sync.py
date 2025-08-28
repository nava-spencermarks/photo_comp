#!/usr/bin/env python3

"""
Test rectangle synchronization functionality between canvas elements.
Tests the JavaScript rectangle drawing and synchronization logic.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app import app


class RectangleSyncTestCase(unittest.TestCase):
    """Test rectangle synchronization between canvas elements."""

    def setUp(self):
        """Set up test client and temporary upload directory."""
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False

        # Create temporary upload directory
        self.temp_upload_dir = tempfile.mkdtemp()
        self.app.config["UPLOAD_FOLDER"] = self.temp_upload_dir

        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_upload_dir, ignore_errors=True)

    def test_rectangle_sync_functions_present(self):
        """Test that rectangle synchronization functions are present in template."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        html_content = response.get_data(as_text=True)

        # Check that synchronization functions are present
        self.assertIn("syncRectangles()", html_content)
        self.assertIn("syncDrawingPreview(", html_content)

        # Check that global drawer variables are defined
        self.assertIn("canvas1_drawer", html_content)
        self.assertIn("canvas2_drawer", html_content)

        # Check for enhanced UX features
        self.assertIn("resizeRectangle(", html_content)
        self.assertIn("drawPreview(", html_content)
        self.assertIn("getResizeHandle(", html_content)

    def test_sync_rectangle_logic_in_javascript(self):
        """Test that the synchronization logic is properly implemented in JavaScript."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        html_content = response.get_data(as_text=True)

        # Verify that sync is called after drawing
        self.assertIn("this.syncRectangles();", html_content)

        # Verify that the syncRectangles function accesses the correct global variables
        self.assertIn("canvas2_drawer : canvas1_drawer", html_content)

        # Verify that scale factors are calculated
        self.assertIn("otherDrawer.canvas.width / this.canvas.width", html_content)
        self.assertIn("otherDrawer.canvas.height / this.canvas.height", html_content)

    def test_drawing_preview_sync_functionality(self):
        """Test that drawing preview synchronization is implemented."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        html_content = response.get_data(as_text=True)

        # Check that syncDrawingPreview is called during drawing
        self.assertIn("this.syncDrawingPreview(width, height);", html_content)

        # Check that syncDrawingPreview function exists
        self.assertIn("syncDrawingPreview(width, height)", html_content)

        # Check that it draws on the other canvas
        self.assertIn(
            "otherCtx.fillRect(scaledStartX, scaledStartY, scaledWidth, scaledHeight);",
            html_content,
        )

    def test_rectangle_drawer_initialization(self):
        """Test that RectangleDrawer class is properly initialized."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        html_content = response.get_data(as_text=True)

        # Check RectangleDrawer constructor
        self.assertIn("class RectangleDrawer", html_content)
        self.assertIn("constructor(canvasId, imageId)", html_content)

        # Check that both drawers are created
        self.assertIn(
            "canvas1_drawer = new RectangleDrawer(canvasId, previewId);", html_content
        )
        self.assertIn(
            "canvas2_drawer = new RectangleDrawer(canvasId, previewId);", html_content
        )

    def test_event_listener_setup(self):
        """Test that event listeners are properly set up for synchronization."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        html_content = response.get_data(as_text=True)

        # Check that mouse event handlers are set up
        self.assertIn("handleMouseDown", html_content)
        self.assertIn("handleMouseMove", html_content)
        self.assertIn("handleMouseUp", html_content)

        # Check that synchronization happens on mouse events
        self.assertIn("syncRectangles()", html_content)

    def test_canvas_scaling_calculation(self):
        """Test that canvas scaling for different image sizes is handled."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        html_content = response.get_data(as_text=True)

        # Check scaling factors are properly calculated
        self.assertIn("scaleX", html_content)
        self.assertIn("scaleY", html_content)

        # Check that rectangles are scaled when synchronized
        self.assertIn("x: rect.x * scaleX", html_content)
        self.assertIn("y: rect.y * scaleY", html_content)
        self.assertIn("width: rect.width * scaleX", html_content)
        self.assertIn("height: rect.height * scaleY", html_content)


if __name__ == "__main__":
    unittest.main()
