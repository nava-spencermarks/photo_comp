#!/usr/bin/env python3
"""
Simple Flask web app for face comparison.
"""

import os
import tempfile
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Import after path modification  # noqa: E402
from src.face_compare import FaceComparator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def allowed_file(filename):
    """Check if uploaded file has allowed extension."""
    if not filename or '.' not in filename:
        return False
    
    # Split filename and extension
    parts = filename.rsplit('.', 1)
    if len(parts) != 2:
        return False
    
    name, ext = parts
    return name != '' and ext.lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page with upload form."""
    return render_template('index.html')


@app.route('/compare', methods=['POST'])
def compare_faces():
    """Handle face comparison request."""
    # Check if files were uploaded
    if 'image1' not in request.files or 'image2' not in request.files:
        flash('Please select both images')
        return redirect(url_for('index'))
    
    file1 = request.files['image1']
    file2 = request.files['image2']
    
    # Check if files were actually selected
    if file1.filename == '' or file2.filename == '':
        flash('Please select both images')
        return redirect(url_for('index'))
    
    # Check file types
    if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
        flash('Please upload valid image files (PNG, JPG, JPEG, GIF, BMP)')
        return redirect(url_for('index'))
    
    try:
        # Save uploaded files
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        
        file1.save(filepath1)
        file2.save(filepath2)
        
        # Perform face comparison
        comparator = FaceComparator()
        is_same_person, details = comparator.compare_faces(filepath1, filepath2)
        
        # Prepare result data
        result_data = {
            'image1': filename1,
            'image2': filename2,
            'is_same_person': is_same_person,
            'details': details,
            'confidence': 'High' if 'Distance: 0.' in details else 'Medium'
        }
        
        return render_template('result.html', **result_data)
        
    except Exception as e:
        flash(f'Error processing images: {str(e)}')
        return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)