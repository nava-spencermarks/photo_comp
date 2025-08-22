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
        sys.exit(1)
    
    image1_path = sys.argv[1]
    image2_path = sys.argv[2]
    
    comparator = RobustFaceComparator()
    is_same_person, details = comparator.compare_faces(image1_path, image2_path)

if __name__ == "__main__":
    main()