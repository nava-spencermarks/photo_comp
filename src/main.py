#!/usr/bin/env python3
"""
Face Comparison Application
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))
from face_compare import RobustFaceComparator


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <image1_path> <image2_path>")
        print("\nCompares two images to determine if they contain the same person.")
        sys.exit(1)

    image1_path = sys.argv[1]
    image2_path = sys.argv[2]

    print(f"Comparing {image1_path} vs {image2_path}")
    
    comparator = RobustFaceComparator()
    is_same_person, details = comparator.compare_faces(image1_path, image2_path)
    
    if is_same_person:
        print(f"✅ SAME PERSON (confidence: {details.get('confidence', 0):.1f}%)")
    else:
        print(f"❌ DIFFERENT PEOPLE (distance: {details.get('distance', 'N/A')})")


if __name__ == "__main__":
    main()
