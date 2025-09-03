# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set maintainer info
LABEL maintainer="Face Comparison Tool"
LABEL description="Flask web application for AI-powered face comparison with interactive masking"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Install system dependencies required for face recognition and OpenCV
RUN apt-get update && apt-get install -y \
    # OpenCV dependencies
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    # face_recognition dependencies
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    # Image processing
    libjpeg62-turbo-dev \
    libpng-dev \
    libtiff5-dev \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Set work directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
# Install main dependencies first, then dev dependencies (optional)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    # Clean up pip cache
    pip cache purge

# Create necessary directories
RUN mkdir -p uploads logs templates static src test

# Copy application code
COPY . .

# Create a non-root user for security
RUN groupadd -r appuser && \
    useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the application port (8060 - NEVER CHANGE!)
EXPOSE 8060

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8060/', timeout=10)" || exit 1

# Set the default command
CMD ["python", "app.py"]