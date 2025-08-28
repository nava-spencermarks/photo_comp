#!/usr/bin/env python3
"""
Simple Flask web app for face comparison.
"""

import os
import tempfile
import logging
import json
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Import after path modification  # noqa: E402
from src.face_compare import FaceComparator
from src.image_masking import ImageMasker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['LOG_FOLDER'] = 'logs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create directories if they don't exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['LOG_FOLDER']).mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(app.config['LOG_FOLDER'], 'app.log')),
        logging.StreamHandler()
    ]
)

# Create user activity logger
activity_logger = logging.getLogger('user_activity')
activity_handler = logging.FileHandler(os.path.join(app.config['LOG_FOLDER'], 'user_activity.log'))
activity_formatter = logging.Formatter('%(asctime)s - %(message)s')
activity_handler.setFormatter(activity_formatter)
activity_logger.addHandler(activity_handler)
activity_logger.setLevel(logging.INFO)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def log_user_activity(action, details=None, ip_address=None):
    """Log user activity with timestamp, IP, and action details."""
    if ip_address is None:
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'ip_address': ip_address,
        'action': action,
        'details': details or {},
        'user_agent': request.headers.get('User-Agent', 'unknown')
    }
    
    activity_logger.info(json.dumps(log_entry))


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
    log_user_activity('page_visit', {'page': 'index'})
    return render_template('index.html')


@app.route('/compare', methods=['POST'])
def compare_faces():
    """Handle face comparison request."""
    log_user_activity('face_comparison_attempt')
    
    # Check if files were uploaded
    if 'image1' not in request.files or 'image2' not in request.files:
        flash('Please select both images')
        log_user_activity('face_comparison_failed', {'reason': 'missing_files'})
        return redirect(url_for('index'))
    
    file1 = request.files['image1']
    file2 = request.files['image2']
    
    # Check if files were actually selected
    if file1.filename == '' or file2.filename == '':
        flash('Please select both images')
        log_user_activity('face_comparison_failed', {'reason': 'empty_filenames'})
        return redirect(url_for('index'))
    
    # Check file types
    if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
        flash('Please upload valid image files (PNG, JPG, JPEG, GIF, BMP)')
        log_user_activity('face_comparison_failed', {'reason': 'invalid_file_types', 'files': [file1.filename, file2.filename]})
        return redirect(url_for('index'))
    
    try:
        # Save uploaded files
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        
        file1.save(filepath1)
        file2.save(filepath2)
        
        # Get rectangle data from form
        rectangles1_json = request.form.get('rectangles1', '')
        rectangles2_json = request.form.get('rectangles2', '')
        
        # Initialize masker and parse rectangle data
        masker = ImageMasker()
        rectangles1 = masker.parse_rectangle_data(rectangles1_json)
        rectangles2 = masker.parse_rectangle_data(rectangles2_json)
        
        # Determine comparison images (original or masked)
        comparison_filepath1 = filepath1
        comparison_filepath2 = filepath2
        mask_applied = False
        
        # Apply masks if rectangles are present
        if rectangles1 or rectangles2:
            # Create masked versions
            masked_filename1 = f"masked_{filename1}"
            masked_filename2 = f"masked_{filename2}"
            
            masked_filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], masked_filename1)
            masked_filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], masked_filename2)
            
            # Apply masks (use same rectangles for both images for synchronized masking)
            # Use rectangles1 as primary, fall back to rectangles2
            primary_rectangles = rectangles1 if rectangles1 else rectangles2
            
            masker.create_masked_image_file(filepath1, masked_filepath1, primary_rectangles)
            masker.create_masked_image_file(filepath2, masked_filepath2, primary_rectangles)
            
            comparison_filepath1 = masked_filepath1
            comparison_filepath2 = masked_filepath2
            mask_applied = True
        
        # Perform face comparison
        comparator = FaceComparator()
        is_same_person, details = comparator.compare_faces(comparison_filepath1, comparison_filepath2)
        
        # Get mask statistics if masks were applied
        mask_stats = None
        if mask_applied:
            primary_rectangles = rectangles1 if rectangles1 else rectangles2
            mask = masker.create_mask_from_rectangles(filepath1, primary_rectangles)
            mask_stats = masker.get_mask_statistics(mask)
        
        # Prepare result data
        result_data = {
            'image1': filename1,
            'image2': filename2,
            'is_same_person': is_same_person,
            'details': details,
            'confidence': 'High' if 'Distance: 0.' in details else 'Medium',
            'mask_applied': mask_applied,
            'mask_stats': mask_stats,
            'rectangles_count': len(rectangles1) if rectangles1 else len(rectangles2) if rectangles2 else 0
        }
        
        # Log successful comparison
        log_user_activity('face_comparison_success', {
            'files': [filename1, filename2],
            'result': is_same_person,
            'mask_applied': mask_applied,
            'rectangles_count': result_data['rectangles_count']
        })
        
        return render_template('result.html', **result_data)
        
    except Exception as e:
        flash(f'Error processing images: {str(e)}')
        log_user_activity('face_comparison_error', {'error': str(e)})
        return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    from flask import send_from_directory
    log_user_activity('file_access', {'filename': filename})
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/admin/logs')
def view_logs():
    """View user activity logs (admin only)."""
    log_user_activity('admin_logs_access')
    
    try:
        log_file = os.path.join(app.config['LOG_FOLDER'], 'user_activity.log')
        logs = []
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            # Parse the log line (timestamp - json_data)
                            parts = line.strip().split(' - ', 1)
                            if len(parts) == 2:
                                timestamp_str, json_str = parts
                                log_data = json.loads(json_str)
                                logs.append(log_data)
                        except json.JSONDecodeError:
                            continue
        
        # Sort by timestamp descending (most recent first)
        logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return render_template('logs.html', logs=logs)
        
    except Exception as e:
        flash(f'Error reading logs: {str(e)}')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8060)
