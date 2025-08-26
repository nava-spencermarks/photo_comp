#!/usr/bin/env python3
"""
Robust face comparison with multiple fallback detection strategies.
"""

import warnings

warnings.filterwarnings(
    "ignore", category=UserWarning, module="face_recognition_models"
)

import face_recognition
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os


class FaceComparator:
    def __init__(self, tolerance=0.45):
        self.tolerance = tolerance
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    @staticmethod
    def preprocess_image_variations(image_path):
        """Create multiple variations of an image for better detection."""
        original_image = face_recognition.load_image_file(image_path)
        pil_image = Image.fromarray(original_image)

        # Convert RGBA to RGB if needed
        if pil_image.mode == "RGBA":
            pil_image = pil_image.convert("RGB")
            original_image = np.array(pil_image)

        variations = []

        # Original resized
        if max(pil_image.size) > 1200:
            ratio = 1200 / max(pil_image.size)
            new_size = (int(pil_image.width * ratio), int(pil_image.height * ratio))
            resized = pil_image.resize(new_size, Image.Resampling.LANCZOS)
            variations.append(("Original resized", np.array(resized)))
        else:
            variations.append(("Original", original_image))

            # Enhanced contrast

            enhanced = ImageEnhance.Contrast(pil_image).enhance(1.3)
            if max(enhanced.size) > 1200:
                ratio = 1200 / max(enhanced.size)
                new_size = (int(enhanced.width * ratio), int(enhanced.height * ratio))
                enhanced = enhanced.resize(new_size, Image.Resampling.LANCZOS)
            variations.append(("Enhanced contrast", np.array(enhanced)))

            # Brightened
            brightened = ImageEnhance.Brightness(pil_image).enhance(1.2)
            if max(brightened.size) > 1200:
                ratio = 1200 / max(brightened.size)
                new_size = (
                    int(brightened.width * ratio),
                    int(brightened.height * ratio),
                )
                brightened = brightened.resize(new_size, Image.Resampling.LANCZOS)
            variations.append(("Brightened", np.array(brightened)))

            # Smaller version (sometimes helps)

            smaller = pil_image.resize(
                (pil_image.width // 2, pil_image.height // 2), Image.Resampling.LANCZOS
            )
            variations.append(("Smaller", np.array(smaller)))

        return variations

    def detect_with_opencv_fallback(self, image_np):
        """Use OpenCV as fallback detection, but be more conservative."""
        try:
            cv_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            # Conservative parameters to avoid false positives
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=6,  # Higher requirement
                minSize=(80, 80),  # Larger minimum
                maxSize=(400, 400),  # Reasonable maximum
                flags=cv2.CASCADE_SCALE_IMAGE,
            )

            # Filter by aspect ratio more strictly
            good_faces = []
            for x, y, w, h in faces:
                aspect_ratio = w / h
                if 0.8 <= aspect_ratio <= 1.25:  # More strict proportions
                    good_faces.append(
                        (y, x + w, y + h, x)
                    )  # Convert to face_recognition format

            return good_faces
        except:
            return []

    def get_face_encodings(self, image_path):
        """Get face encodings with multiple fallback strategies."""
        print(f"Analyzing {os.path.basename(image_path)}...")

        # Try multiple image variations
        variations = self.preprocess_image_variations(image_path)

        for var_name, image_np in variations:
            print(f"  Trying {var_name}...")

            # Strategy 1: face_recognition HOG

            face_locations = face_recognition.face_locations(
                image_np, model="hog", number_of_times_to_upsample=1
            )

            if face_locations:
                encodings = face_recognition.face_encodings(image_np, face_locations)
                if encodings:
                    print(f"    ✓ HOG found {len(encodings)} faces")
                    return (
                        encodings,
                        f"Found {len(encodings)} faces using HOG on {var_name}",
                    )

        # Strategy 2: face_recognition HOG with more upsampling
        try:
            face_locations = face_recognition.face_locations(
                image_np, model="hog", number_of_times_to_upsample=2
            )
            if face_locations:
                encodings = face_recognition.face_encodings(image_np, face_locations)
                if encodings:
                    print(f"    ✓ HOG 2x found {len(encodings)} faces")
                    return (
                        encodings,
                        f"Found {len(encodings)} faces using HOG 2x on {var_name}",
                    )
        except Exception as e:
            print(f"    HOG 2x failed: {e}")

        # Strategy 3: face_recognition CNN (slower but more accurate)

            face_locations = face_recognition.face_locations(image_np, model="cnn")
            if face_locations:
                encodings = face_recognition.face_encodings(image_np, face_locations)
                if encodings:
                    print(f"    ✓ CNN found {len(encodings)} faces")
                    return (
                        encodings,
                        f"Found {len(encodings)} faces using CNN on {var_name}",
                    )


        # Strategy 4: OpenCV fallback (conservative)
        opencv_faces = self.detect_with_opencv_fallback(image_np)
        if opencv_faces:

                encodings = face_recognition.face_encodings(image_np, opencv_faces)
                if encodings:
                    print(f"    ✓ OpenCV fallback found {len(encodings)} faces")
                    return (
                        encodings,
                        f"Found {len(encodings)} faces using OpenCV fallback on {var_name}",
                    )

        return None, "No faces detected with any method or image variation"


    def compare_faces(self, image1_path, image2_path):
        """Compare faces between two images with robust detection."""
        print(
            f"Comparing {os.path.basename(image1_path)} vs {os.path.basename(image2_path)}"
        )
        print("=" * 60)

        encodings1, msg1 = self.get_face_encodings(image1_path)
        print(f"Image 1: {msg1}\n")

        encodings2, msg2 = self.get_face_encodings(image2_path)
        print(f"Image 2: {msg2}\n")

        if encodings1 is None or encodings2 is None:
            print("❌ CANNOT COMPARE - Face detection failed")
            if encodings1 is None:
                print(f"   • Image 1: {msg1}")
            if encodings2 is None:
                print(f"   • Image 2: {msg2}")
            print("\n💡 Try images with:")
            print("   • Clear, well-lit faces")
            print("   • Frontal view (not profile)")
            print("   • Faces at least 100x100 pixels")
            print("   • Good contrast")
            return False, "Face detection failed"

        print(f"Comparing {len(encodings1)} faces vs {len(encodings2)} faces...")

        # Compare all face combinations
        best_distance = float("inf")
        matches = []

        for i, enc1 in enumerate(encodings1):
            for j, enc2 in enumerate(encodings2):
                distance = face_recognition.face_distance([enc1], enc2)[0]
                if distance <= self.tolerance:
                    matches.append((i + 1, j + 1, distance))
                if distance < best_distance:
                    best_distance = distance

        is_match = len(matches) > 0
        confidence = (
            max(0, (self.tolerance - best_distance) / self.tolerance * 100)
            if best_distance != float("inf")
            else 0
        )

        print("\n" + "=" * 60)
        print("FINAL RESULT:")
        print("-" * 60)
        print(f"Best match distance: {best_distance:.3f}")
        print(f"Similarity threshold: {self.tolerance}")
        print(f"Confidence: {confidence:.1f}%")

        if is_match:
            print(f"✅ SAME PERSON")
            print(f"   {len(matches)} matching face pair(s) found:")
            for face1, face2, dist in matches[:3]:
                print(f"   • Face {face1} ↔ Face {face2} (distance: {dist:.3f})")
            if len(matches) > 3:
                print(f"   ... and {len(matches) - 3} more")
        else:
            print(f"❌ DIFFERENT PEOPLE")
            if best_distance != float("inf"):
                print(f"   Closest similarity: {best_distance:.3f} (above threshold)")
            else:
                print(f"   No measurable similarity found")

        print("=" * 60)
        return is_match, f"Distance: {best_distance:.3f}, Confidence: {confidence:.1f}%"
