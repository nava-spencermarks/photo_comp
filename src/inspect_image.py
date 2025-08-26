#!/usr/bin/env python3
"""
Tool to inspect what's actually in the images and why face detection might be failing.
"""

import os

import cv2
import face_recognition
import numpy as np
from PIL import Image


def inspect_image(image_path):
    """Inspect an image to understand why face detection might fail."""
    print(f"\n🔍 INSPECTING: {os.path.basename(image_path)}")
    print("=" * 50)

    if not os.path.exists(image_path):
        print("❌ File does not exist")
        return

    # Basic file info
    file_size = os.path.getsize(image_path)
    print(f"File size: {file_size:,} bytes")

    try:
        # Load with PIL
        pil_image = Image.open(image_path)
        print(f"Image dimensions: {pil_image.size[0]} x {pil_image.size[1]} pixels")
        print(f"Image mode: {pil_image.mode}")

        # Load with face_recognition
        fr_image = face_recognition.load_image_file(image_path)
        print(f"Face_recognition shape: {fr_image.shape}")

        # Check if it's too large
        if max(pil_image.size) > 3000:
            print("⚠️  Image is very large - might need more aggressive resizing")

        # Try to assess image quality
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(fr_image, cv2.COLOR_RGB2GRAY)

        # Calculate some basic metrics
        mean_brightness = np.mean(gray)
        contrast = np.std(gray)

        print(f"Average brightness: {mean_brightness:.1f}/255")
        print(f"Contrast (std dev): {contrast:.1f}")

        if mean_brightness < 50:
            print("⚠️  Image appears very dark")
        elif mean_brightness > 200:
            print("⚠️  Image appears very bright")

        if contrast < 20:
            print("⚠️  Image has very low contrast")

        # Try different OpenCV detection settings to see if we can find ANYTHING
        print("\n🔍 OpenCV Detection Tests:")
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        test_params = [
            ("Very permissive", 1.05, 1, (20, 20)),
            ("Permissive", 1.1, 2, (30, 30)),
            ("Normal", 1.1, 3, (40, 40)),
            ("Conservative", 1.2, 5, (60, 60)),
        ]

        for name, scale, neighbors, min_size in test_params:
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=scale,
                minNeighbors=neighbors,
                minSize=min_size,
                flags=cv2.CASCADE_SCALE_IMAGE,
            )
            print(f"  {name}: {len(faces)} potential faces")
            if 0 < len(faces) < 20:  # Show details if reasonable number
                for i, (x, y, w, h) in enumerate(faces[:5]):  # Max 5
                    print(f"    Face {i+1}: {w}x{h} at ({x},{y})")

        # Try face_recognition with very small image
        print("\n🔍 Face_recognition Tests:")

        # Test with smaller version
        small_image = pil_image.resize((400, 300), Image.Resampling.LANCZOS)
        small_np = np.array(small_image)

        try:
            faces_hog = face_recognition.face_locations(
                small_np, model="hog", number_of_times_to_upsample=0
            )
            print(f"  HOG on small image: {len(faces_hog)} faces")
        except Exception as e:
            print(f"  HOG on small image: Error - {e}")

        try:
            faces_cnn = face_recognition.face_locations(small_np, model="cnn")
            print(f"  CNN on small image: {len(faces_cnn)} faces")
        except Exception as e:
            print(f"  CNN on small image: Error - {e}")

    except Exception as e:
        print(f"❌ Error loading image: {e}")


def main():
    # Check all images in directory
    image_files = [
        f
        for f in os.listdir("..")
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff"))
    ]

    for img_file in sorted(image_files):
        inspect_image(img_file)


if __name__ == "__main__":
    main()
