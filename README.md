# Face Comparison Tool 👥

A robust Python application that compares faces in two images to determine if they show the same person.

## ✨ Features

- **Accurate face detection** using multiple algorithms (HOG, CNN, OpenCV fallback)
- **Robust preprocessing** with multiple image variations for better detection
- **Strict similarity matching** to avoid false positives
- **Clean, human-readable output** with confidence scores
- **Handles various image formats** (PNG, JPG, JPEG, etc.)
- **Comprehensive error handling** with helpful user guidance

## 🚀 Quick Start

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Program

**Compare two images:**
```bash
python src/main.py image1.png image2.png
```

**Example:**
```bash
python src/main.py test/test_data/face_me_1.png test/test_data/me_different.png
```

**Output:**
```
Comparing face_me_1.png vs me_different.png
============================================================
Analyzing face_me_1.png...
  ✓ HOG found 1 faces
Image 1: Found 1 faces using HOG on Original resized

Analyzing me_different.png...
  ✓ HOG found 1 faces  
Image 2: Found 1 faces using HOG on Original

Comparing 1 faces vs 1 faces...

============================================================
FINAL RESULT:
------------------------------------------------------------
Best match distance: 0.579
Similarity threshold: 0.45
Confidence: 0.0%
❌ DIFFERENT PEOPLE
   Closest similarity: 0.579 (above threshold)
============================================================
```

## 🧪 Running Tests

### Run All Tests
```bash
cd test
python run_all_tests.py
```

### Run Individual Test Suites
```bash
cd test

# Test core face comparison logic
python test_face_compare.py

# Test main script functionality  
python test_main.py
```

### Test Output Example
```
🧪 RUNNING ALL TESTS FOR FACE COMPARISON SYSTEM
============================================================

📋 Robust Face Comparison Tests
----------------------------------------
...
✅ All tests passed!

📋 Main Script Tests  
----------------------------------------
...
✅ All tests passed!

🎉 ALL TESTS PASSED!
Your face comparison system is working correctly.
```

## 📋 How It Works

1. **Multi-strategy face detection:**
   - Tries HOG (fast), HOG 2x (thorough), CNN (accurate), and OpenCV fallback
   - Tests multiple image preprocessed variations (contrast, brightness, size)

2. **Facial encoding:**
   - Uses dlib's face recognition models to create unique facial fingerprints
   - Filters out poor quality encodings to avoid false positives

3. **Comparison:**
   - Compares all face pairs between the two images
   - Uses strict similarity threshold (0.45) to minimize false matches
   - Reports confidence percentage and detailed results

## 📁 Project Structure

```
photo-comp/
├── README.md                   # This file
├── requirements.txt            # Dependencies
├── docs/                       # Documentation
│   └── git_setup.md           # GitHub setup guide
├── src/                        # Source code
│   ├── main.py                # Entry point
│   ├── robust_face_compare.py # Core face comparison logic
│   └── inspect_image.py       # Debug utility
└── test/                      # Test suite
    ├── run_all_tests.py       # Test runner
    ├── test_robust_face_compare.py  # Core logic tests
    ├── test_main.py           # Main script tests
    └── test_data/             # Test images
        ├── face_me_1.png     # Sample face image
        ├── me_different.png  # Sample different person
        ├── no_faces_1.png    # Image with no faces
        └── ...               # Additional test images
```

## 💡 Usage Tips

### For Best Results, Use Images With:
- **Clear, well-lit faces**
- **Frontal view** (not profile)
- **Faces at least 100x100 pixels**
- **Good contrast**
- **Standard formats** (PNG, JPG, JPEG)

### Common Results:

**✅ Same Person:**
```
✅ SAME PERSON
   1 matching face pair(s) found:
   • Face 1 ↔ Face 1 (distance: 0.000)
```

**❌ Different People:**
```
❌ DIFFERENT PEOPLE
   Closest similarity: 0.796 (above threshold)
```

**⚠️ No Faces Detected:**
```
❌ CANNOT COMPARE - Face detection failed
   • Image 1: No faces detected with any method

💡 Try images with:
   • Clear, well-lit faces
   • Frontal view (not profile)  
   • Faces at least 100x100 pixels
   • Good contrast
```

## 🔧 Configuration

### Adjust Similarity Threshold

Edit `src/robust_face_compare.py` and modify the tolerance parameter:

```python
# Stricter matching (fewer false positives)
comparator = FaceComparator(tolerance=0.3)

# More lenient matching  
comparator = FaceComparator(tolerance=0.6)
```

**Default:** `0.45` (recommended for accuracy)

## 🐛 Troubleshooting

### "No faces detected"
- Check image quality and lighting
- Ensure faces are clearly visible and frontal
- Try with different photos

### Installation Issues
```bash
# If face_recognition fails to install:
pip install cmake
pip install dlib
pip install face_recognition

# Or install all requirements:
pip install -r requirements.txt
```

### Performance Issues
- Large images are automatically resized
- CNN detection is slower but more accurate
- Use smaller images (< 2MB) for faster processing

## 🧪 Testing

The project includes comprehensive tests covering:

- ✅ **Unit tests** - Individual component functionality
- ✅ **Integration tests** - End-to-end workflows  
- ✅ **Edge cases** - Error handling, missing files, no faces
- ✅ **Real image tests** - Actual face comparison scenarios

Run tests before deploying or after making changes:
```bash
cd test
python run_all_tests.py
```

## 📦 Dependencies

- `face_recognition` - Face detection and encoding
- `opencv-python` - Computer vision fallback detection  
- `numpy` - Numerical operations
- `pillow` - Image processing
- `setuptools` - Package utilities

## 🔒 Security Note

This tool is designed for **defensive security analysis only**. It helps with:
- Identity verification
- Duplicate detection  
- Security analysis

**Do not use for malicious purposes.**

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Run tests to verify installation: `cd test && python run_all_tests.py`
3. Use the debug utility: `python src/inspect_image.py`

**Happy face comparing! 🎭**