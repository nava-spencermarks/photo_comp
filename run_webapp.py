#!/usr/bin/env python3
"""
Simple script to run the Flask web application.
"""

import os
import sys

if __name__ == '__main__':
    # Check if Flask is installed
    try:
        import flask
    except ImportError:
        print("Flask is not installed. Installing...")
        os.system(f"{sys.executable} -m pip install flask>=2.3.0")
    
    # Import and run the app
    from app import app
    
    print("🚀 Starting Face Comparison Web App...")
    print("📱 Open your browser and go to: http://localhost:8060")
    print("🛑 Press Ctrl+C to stop the server")
    
    # DO NOT CHANGE PORT 8060 - This is the permanent default port for this application
    app.run(debug=True, host='0.0.0.0', port=8060)