# 🔍 Face Comparison Web App

A simple, beautiful web application for comparing faces in two images to determine if they contain the same person.

## Features

✅ **Simple Upload Interface**: Drag and drop or browse to select images  
✅ **Side-by-Side Display**: View both images clearly during comparison  
✅ **AI-Powered Analysis**: Uses advanced face recognition technology  
✅ **Instant Results**: Get immediate feedback with confidence levels  
✅ **Responsive Design**: Works on desktop, tablet, and mobile devices  
✅ **Multiple Formats**: Supports PNG, JPG, JPEG, GIF, and BMP files  

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Web App
```bash
python run_webapp.py
```

### 3. Open Your Browser
Navigate to: http://localhost:5000

## Usage

1. **Upload Images**: Select two images containing faces
2. **Compare**: Click "Compare Faces" button
3. **View Results**: See side-by-side comparison with AI analysis
4. **Interpret**: Green = Same Person, Red = Different People

## How It Works

The web app uses the same robust face comparison engine as the command-line tool:

- **Multi-Strategy Detection**: HOG, CNN, and OpenCV fallback methods
- **Advanced Preprocessing**: Image enhancement and multiple variations
- **Precise Measurements**: Facial feature encoding and distance calculation
- **Confidence Scoring**: Based on detection quality and similarity metrics

## Web App Architecture

```
📁 Face Comparison Web App
├── 🐍 app.py              # Flask application
├── 🏃 run_webapp.py       # Startup script
├── 📁 templates/          # HTML templates
│   ├── base.html         # Base template with styling
│   ├── index.html        # Upload page
│   └── result.html       # Results page
├── 📁 uploads/           # Temporary image storage
└── 📁 src/               # Face comparison engine
```

## API Endpoints

- `GET /` - Main upload page
- `POST /compare` - Face comparison (form data with image files)
- `GET /uploads/<filename>` - Serve uploaded images

## Security Notes

- File uploads are validated for type and size
- Filenames are sanitized using `secure_filename()`
- Maximum file size: 16MB
- Temporary file storage in `uploads/` directory

## Customization

### Styling
Edit `templates/base.html` for custom CSS styling.

### File Limits
Modify `MAX_CONTENT_LENGTH` in `app.py` to change upload limits.

### Results Display
Customize `templates/result.html` for different result presentations.

## Troubleshooting

### Port Already in Use
```bash
# Application runs on port 8060 (default and permanent)
python run_webapp.py
```

### Memory Issues
- Reduce image file sizes
- Lower `MAX_CONTENT_LENGTH` setting
- Restart the application periodically

### Face Detection Issues
- Ensure images contain clear, visible faces
- Try different lighting or angles
- Check supported image formats

## Development Mode

The web app runs in debug mode by default, which provides:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

For production deployment, set `debug=False` in `app.py`.

## Performance Tips

- Use reasonably sized images (< 2MB recommended)
- Close browser tabs when not in use
- Clear the `uploads/` folder periodically
- Monitor system memory usage

Enjoy comparing faces with this simple and powerful web interface! 🚀