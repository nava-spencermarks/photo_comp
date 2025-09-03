#!/usr/bin/env python3
"""
Image masking functionality for rectangle-based selective comparison.
"""

import json
from typing import Dict, List, Tuple

import numpy as np
from PIL import Image, ImageDraw


class ImageMasker:
    """Handle image masking operations with rectangle-based masks."""

    def __init__(self):
        """Initialize the image masker."""
        pass

    def parse_rectangle_data(self, rectangle_json: str) -> List[Dict[str, float]]:
        """
        Parse rectangle data from JSON string.

        Args:
            rectangle_json: JSON string containing rectangle data

        Returns:
            List of rectangle dictionaries with normalized coordinates
        """
        if not rectangle_json:
            return []

        try:
            rectangles = json.loads(rectangle_json)

            # Validate rectangle data
            valid_rectangles = []
            for rect in rectangles:
                if all(key in rect for key in ["x", "y", "width", "height"]):
                    # Clamp coordinates to valid range instead of rejecting
                    # This handles rectangles that might slightly exceed bounds
                    x = max(0.0, min(1.0, rect["x"]))
                    y = max(0.0, min(1.0, rect["y"]))

                    # Adjust width and height to stay within bounds
                    # If x is at the edge, width needs to be 0
                    max_width = 1.0 - x
                    max_height = 1.0 - y

                    clamped_rect = {
                        "x": x,
                        "y": y,
                        "width": max(0.0, min(max_width, rect["width"])),
                        "height": max(0.0, min(max_height, rect["height"])),
                    }

                    # Only add if rectangle has positive area after clamping
                    if clamped_rect["width"] > 0 and clamped_rect["height"] > 0:
                        valid_rectangles.append(clamped_rect)
            return valid_rectangles

        except (json.JSONDecodeError, TypeError, KeyError):
            return []

    def create_mask_from_rectangles(
        self, image_path: str, rectangles: List[Dict[str, float]]
    ) -> np.ndarray:
        """
        Create a binary mask from rectangle data.

        Args:
            image_path: Path to the image file
            rectangles: List of rectangle dictionaries with normalized coordinates

        Returns:
            Binary mask as numpy array (True for masked areas, False for unmasked)
        """
        # Load image to get dimensions
        with Image.open(image_path) as img:
            width, height = img.size

        # Create mask (False = unmasked, True = masked)
        mask = np.zeros((height, width), dtype=bool)

        if not rectangles:
            return mask

        # Convert to PIL Image for drawing
        mask_img = Image.new("L", (width, height), 0)  # Black background
        draw = ImageDraw.Draw(mask_img)

        # Draw white rectangles for masked areas
        for rect in rectangles:
            # Clamp normalized coordinates to valid range [0, 1]
            rect_x = max(0.0, min(1.0, rect["x"]))
            rect_y = max(0.0, min(1.0, rect["y"]))
            rect_width = max(0.0, min(1.0 - rect_x, rect["width"]))
            rect_height = max(0.0, min(1.0 - rect_y, rect["height"]))

            # Convert normalized coordinates to pixel coordinates
            x1 = int(rect_x * width)
            y1 = int(rect_y * height)
            x2 = int((rect_x + rect_width) * width)
            y2 = int((rect_y + rect_height) * height)

            # Final bounds check to ensure we're within image
            x1 = max(0, min(x1, width - 1))
            y1 = max(0, min(y1, height - 1))
            x2 = max(x1 + 1, min(x2, width))  # Ensure x2 > x1
            y2 = max(y1 + 1, min(y2, height))  # Ensure y2 > y1

            # Only draw if rectangle has positive area
            if x2 > x1 and y2 > y1:
                draw.rectangle([x1, y1, x2 - 1, y2 - 1], fill=255)

        # Convert back to numpy array
        mask = np.array(mask_img) > 0

        return mask

    def apply_mask_to_image(
        self,
        image_path: str,
        mask: np.ndarray,
        mask_color: Tuple[int, int, int] = (0, 0, 0),
    ) -> Image.Image:
        """
        Apply mask to an image, setting masked areas to specified color.

        Args:
            image_path: Path to the image file
            mask: Binary mask array
            mask_color: RGB color for masked areas (default: black)

        Returns:
            PIL Image with mask applied
        """
        # Load image
        img = Image.open(image_path).convert("RGB")
        img_array = np.array(img)

        # Resize mask to match image if necessary
        if mask.shape != img_array.shape[:2]:
            mask_img = Image.fromarray(mask.astype(np.uint8) * 255)
            mask_img = mask_img.resize(
                (img.width, img.height), Image.Resampling.NEAREST
            )
            mask = np.array(mask_img) > 0

        # Apply mask
        masked_img = img_array.copy()
        masked_img[mask] = mask_color

        return Image.fromarray(masked_img)

    def create_masked_image_file(
        self,
        input_path: str,
        output_path: str,
        rectangles: List[Dict[str, float]],
        mask_color: Tuple[int, int, int] = (0, 0, 0),
    ) -> str:
        """
        Create a masked version of an image and save it to file.

        Args:
            input_path: Path to input image
            output_path: Path to save masked image
            rectangles: List of rectangle dictionaries
            mask_color: RGB color for masked areas

        Returns:
            Path to the created masked image file
        """
        # Create mask
        mask = self.create_mask_from_rectangles(input_path, rectangles)

        # Apply mask to image
        masked_img = self.apply_mask_to_image(input_path, mask, mask_color)

        # Save masked image
        masked_img.save(output_path)

        return output_path

    def get_mask_statistics(self, mask: np.ndarray) -> Dict[str, float]:
        """
        Get statistics about a mask.

        Args:
            mask: Binary mask array

        Returns:
            Dictionary with mask statistics
        """
        total_pixels = mask.size
        masked_pixels = np.sum(mask)
        unmasked_pixels = total_pixels - masked_pixels

        return {
            "total_pixels": int(total_pixels),
            "masked_pixels": int(masked_pixels),
            "unmasked_pixels": int(unmasked_pixels),
            "mask_percentage": (
                float(masked_pixels / total_pixels * 100) if total_pixels > 0 else 0.0
            ),
            "unmasked_percentage": (
                float(unmasked_pixels / total_pixels * 100) if total_pixels > 0 else 0.0
            ),
        }

    def validate_rectangles_match(
        self,
        rectangles1: List[Dict[str, float]],
        rectangles2: List[Dict[str, float]],
        tolerance: float = 0.01,
    ) -> bool:
        """
        Validate that two sets of rectangles match (for synchronized masking).

        Args:
            rectangles1: First set of rectangles
            rectangles2: Second set of rectangles
            tolerance: Tolerance for coordinate differences

        Returns:
            True if rectangles match within tolerance
        """
        if len(rectangles1) != len(rectangles2):
            return False

        for r1, r2 in zip(rectangles1, rectangles2):
            for key in ["x", "y", "width", "height"]:
                if abs(r1[key] - r2[key]) > tolerance:
                    return False

        return True
