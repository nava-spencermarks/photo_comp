#!/usr/bin/env python3
"""
Face Comparison Application
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))
from face_compare import FaceComparator


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <image1_path> <image2_path>")
        print("\nCompares two images to determine if they contain the same person.")
        sys.exit(1)

    image1_path = sys.argv[1]
    image2_path = sys.argv[2]

    print(f"Comparing {image1_path} vs {image2_path}")

    comparator = FaceComparator()
    is_same_person, details = comparator.compare_faces(image1_path, image2_path)

    if is_same_person:
        if isinstance(details, dict):
            confidence = details.get('confidence', 0)
            print(f"✅ SAME PERSON (confidence: {confidence:.1f}%)")
        else:
            print(f"✅ SAME PERSON - {details}")
    else:
        if isinstance(details, dict):
            distance = details.get('distance', 'N/A')
            print(f"❌ DIFFERENT PEOPLE (distance: {distance})")
        else:
            print(f"❌ DIFFERENT PEOPLE - {details}")


if __name__ == "__main__":
    main()
