# Face Comparison Tool 👥

A robust Python application with both command-line and web interfaces that compares faces in two images to determine if they show the same person, featuring interactive rectangle masking for precise region-based comparisons.

## ✨ Features

### Core Capabilities
- **Accurate face detection** using multiple algorithms (HOG, CNN, OpenCV fallback)  
- **Robust preprocessing** with multiple image variations for better detection
- **Strict similarity matching** to avoid false positives
- **Clean, human-readable output** with confidence scores
- **Handles various image formats** (PNG, JPG, JPEG, GIF, BMP)
- **Comprehensive error handling** with helpful user guidance

### 🌐 Web Interface NEW!
- **Interactive Flask web application** with drag-and-drop image upload
- **Side-by-side image display** with real-time comparison results
- **Rectangle masking tool** for selective region comparison
- **Responsive modern UI** with intuitive controls
- **Real-time mask statistics** and comparison metrics

### 🎯 Rectangle Masking System NEW!
- **Interactive rectangle drawing** on uploaded images
- **Synchronized masking** - rectangles automatically appear on both images
- **Easy rectangle movement** with hover effects and drag-and-drop
- **Keyboard shortcuts** (D=toggle mode, Del=remove, Esc=cancel)
- **Grid snapping** for precise alignment
- **Multiple selection modes** (draw/move) with visual feedback

## 🚀 Quick Start

### Fresh Installation (Clean Checkout)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd photo-comp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python test_working_coverage.py
   ```

### Usage Options

#### 🌐 Web Interface (Recommended)

**Start the web application:**
```bash
python app.py
```

Then open your browser to: **http://localhost:8080**

**Features:**
- Upload two images using the web interface
- Draw rectangles to mask specific areas (eyes, background, etc.)
- Get real-time comparison results with mask statistics
- Interactive rectangle editing with keyboard shortcuts

#### 💻 Command Line Interface

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

## 🎯 Interactive Rectangle Masking

The web interface includes a powerful rectangle masking system for precise region-based comparisons:

### How to Use Rectangle Masking

1. **Upload Images:** Use the web interface to upload two images
2. **Draw Mode:** Click "✏️ Draw Mode" (default) to draw rectangles
3. **Draw Rectangles:** Click and drag on the image to create mask rectangles
4. **Move Mode:** Click "✋ Move Mode" to move existing rectangles
5. **Fine-tuning:** Hover over rectangles to highlight them, then drag to move
6. **Submit:** Click "🔍 Compare Faces" to run masked comparison

### Rectangle Controls

**Mouse Controls:**
- **Draw Mode:** Click and drag to create new rectangles
- **Move Mode:** Click and drag existing rectangles to reposition
- **Hover Effects:** Rectangles highlight when you hover over them

**Keyboard Shortcuts:**
- **D Key:** Toggle between draw and move modes
- **Delete/Backspace:** Remove the last rectangle
- **Escape:** Cancel current drawing or deselect rectangle

**Visual Features:**
- **Grid Snapping:** Rectangles snap to 5-pixel grid for alignment
- **Size Display:** Real-time size display while drawing (e.g., "120×80")
- **Hover Highlighting:** Rectangles get lighter and thicker borders when hovered
- **Synchronized Masking:** Rectangles automatically appear on both images

### Masking Use Cases

- **Focus on specific facial features** (eyes, nose, mouth)
- **Exclude background elements** that might interfere
- **Mask out accessories** (glasses, hats, jewelry)
- **Compare partial faces** or specific regions
- **Remove lighting inconsistencies** between images

## 🧪 Running Tests

### Run All Tests (Recommended)
```bash
python test_working_coverage.py
```

### Run Individual Test Suites
```bash
# Test core face comparison logic
python test/test_face_compare.py

# Test main script functionality  
python test/test_main.py

# Test web application
python test/test_webapp.py

# Test image masking functionality
python test/test_image_masking.py

# Test rectangle frontend features
python test/test_rectangle_frontend.py
```

### Test Output Example
```
🧪 Running working tests with coverage...
============================================================

========================= test session starts =========================
...
test/test_face_compare.py::TestFaceComparator::test_identical_images PASSED
test/test_webapp.py::WebAppTestCase::test_compare_with_rectangle_data PASSED  
test/test_image_masking.py::ImageMaskingTestCase::test_create_mask_from_rectangles_single PASSED
test/test_rectangle_frontend.py::RectangleDrawerUnitTests::test_rectangle_drawer_methods_defined PASSED
...

========================= 65 passed in 27.22s ========================

📊 Coverage Report:
Current Coverage: 81%
✅ Coverage maintained or improved

✅ All working tests passed with good coverage!
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
├── app.py                     # Flask web application (NEW)
├── run_webapp.py              # Web app launcher script (NEW)
├── test_working_coverage.py   # Comprehensive test runner (NEW)
├── run_coverage.py            # Coverage analysis script (NEW)
├── coverage_tracker.py        # Coverage regression tracking (NEW)
├── WEB_APP_README.md          # Web app documentation (NEW)
├── src/                       # Source code
│   ├── main.py               # Command-line entry point
│   ├── face_compare.py       # Core face comparison logic
│   ├── inspect_image.py      # Debug utility
│   └── image_masking.py      # Rectangle masking system (NEW)
├── templates/                 # Web interface templates (NEW)
│   ├── base.html            # Base template with styling
│   ├── index.html           # Upload and masking interface
│   └── result.html          # Comparison results display
├── uploads/                   # Image upload storage (NEW)
└── test/                     # Comprehensive test suite
    ├── run_all_tests.py      # Legacy test runner
    ├── test_face_compare.py  # Core logic tests
    ├── test_main.py          # Main script tests
    ├── test_inspect_image.py # Debug utility tests
    ├── test_webapp.py        # Web application tests (NEW)
    ├── test_image_masking.py # Masking system tests (NEW)
    ├── test_rectangle_frontend.py # Frontend tests (NEW)
    └── test_data/            # Test images
        ├── face_me_1.png    # Sample face image
        ├── me_different.png # Sample different person
        ├── no_faces_1.png   # Image with no faces
        └── ...              # Additional test images
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

### Web Interface Issues
```bash
# If port 8080 is already in use, edit app.py:
# Change: app.run(debug=True, host='0.0.0.0', port=8080)
# To:     app.run(debug=True, host='0.0.0.0', port=8081)

# If upload fails, check folder permissions:
mkdir -p uploads
chmod 755 uploads
```

### Rectangle Masking Issues
- **Rectangles not appearing:** Ensure both images are loaded before drawing
- **Rectangles not synchronized:** Refresh the page and try again
- **Can't move rectangles:** Toggle to move mode with the button or 'D' key
- **Rectangles too small:** Minimum size is 10x10 pixels

## 🧪 Testing

The project includes comprehensive tests covering:

- ✅ **Unit tests** - Individual component functionality (25 tests)
- ✅ **Integration tests** - End-to-end workflows (18 web app tests)
- ✅ **Edge cases** - Error handling, missing files, no faces
- ✅ **Real image tests** - Actual face comparison scenarios
- ✅ **Web interface tests** - Flask routes and responses (NEW)
- ✅ **Rectangle masking tests** - Image processing and validation (NEW) 
- ✅ **Frontend tests** - JavaScript functionality validation (NEW)

**Total: 65+ tests with 81% code coverage**

Run tests before deploying or after making changes:
```bash
python test_working_coverage.py
```

### Test Categories

1. **Core Face Comparison** (`test_face_compare.py`) - 10 tests
2. **Main Script** (`test_main.py`) - 6 tests  
3. **Image Inspection** (`test_inspect_image.py`) - 9 tests
4. **Web Application** (`test_webapp.py`) - 18 tests
5. **Image Masking** (`test_image_masking.py`) - 14 tests
6. **Rectangle Frontend** (`test_rectangle_frontend.py`) - 8 tests

## 📦 Dependencies

### Core Libraries
- `face_recognition` - Face detection and encoding
- `opencv-python` - Computer vision fallback detection  
- `numpy` - Numerical operations
- `pillow` - Image processing
- `setuptools` - Package utilities

### Web Interface (NEW)
- `flask>=2.3.0` - Web framework for the interactive interface
- `werkzeug` - Flask utilities (included with Flask)

### Testing & Development
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `isort` - Import sorting

All dependencies are automatically installed with:
```bash
pip install -r requirements.txt
```

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
