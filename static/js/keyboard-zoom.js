/**
 * Keyboard Zoom Controls
 * Handles + and - key presses to zoom images in and out
 */

// Zoom state tracking
let zoomLevels = {
    1: 1.0,  // Image 1 zoom level
    2: 1.0   // Image 2 zoom level
};

// Zoom mode tracking (false = free zoom, true = constrained zoom)
let constrainedZoomMode = {
    1: false,  // Image 1 zoom mode
    2: false   // Image 2 zoom mode
};

const MIN_ZOOM = 0.5;
const MAX_ZOOM = 3.0;
const ZOOM_STEP = 0.1;

document.addEventListener('DOMContentLoaded', function() {
    // Add keyboard event listener
    document.addEventListener('keydown', handleKeyboardZoom);
    
    // Add zoom mode toggle event listeners
    const zoomModeButtons = document.querySelectorAll('.btn-zoom-mode');
    zoomModeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const imageId = parseInt(this.dataset.imageId);
            toggleZoomMode(imageId);
        });
    });
    
    console.log('Keyboard zoom controls initialized');
    console.log('Use + (or =) to zoom in, - to zoom out');
    console.log('Click zoom mode button to toggle between Free and Constrained zoom');
});

function handleKeyboardZoom(event) {
    // Only handle zoom if we're not in an input field
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        return;
    }
    
    // Check for zoom keys
    if (event.key === '+' || event.key === '=') {
        event.preventDefault();
        zoomImages(ZOOM_STEP);
    } else if (event.key === '-' || event.key === '_') {
        event.preventDefault();
        zoomImages(-ZOOM_STEP);
    }
}

function zoomImages(deltaZoom) {
    // Get currently visible images
    const img1 = document.getElementById('preview1');
    const img2 = document.getElementById('preview2');
    const container1 = document.getElementById('canvas-container-1');
    const container2 = document.getElementById('canvas-container-2');
    
    let zoomedAny = false;
    
    // Zoom image 1 if visible
    if (container1 && container1.classList.contains('active')) {
        const newZoom = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, zoomLevels[1] + deltaZoom));
        if (newZoom !== zoomLevels[1]) {
            zoomLevels[1] = newZoom;
            applyZoom(img1, 1, newZoom);
            zoomedAny = true;
        }
    }
    
    // Zoom image 2 if visible
    if (container2 && container2.classList.contains('active')) {
        const newZoom = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, zoomLevels[2] + deltaZoom));
        if (newZoom !== zoomLevels[2]) {
            zoomLevels[2] = newZoom;
            applyZoom(img2, 2, newZoom);
            zoomedAny = true;
        }
    }
    
    if (zoomedAny) {
        console.log(`Zoom levels - Image 1: ${zoomLevels[1].toFixed(1)}x, Image 2: ${zoomLevels[2].toFixed(1)}x`);
        updateZoomIndicators();
    }
}

function applyZoom(img, imageNum, zoomLevel) {
    if (!img) return;
    
    const isConstrained = constrainedZoomMode[imageNum];
    
    if (isConstrained) {
        // Constrained zoom: use width/height instead of transform
        const wrapper = img.parentElement;
        if (wrapper) {
            // Calculate new dimensions while maintaining aspect ratio
            const originalWidth = img.naturalWidth;
            const originalHeight = img.naturalHeight;
            const containerMaxWidth = 300; // max-width from CSS
            const containerMaxHeight = 300; // max-height from CSS
            
            // Calculate the original display size
            const aspectRatio = originalWidth / originalHeight;
            let displayWidth, displayHeight;
            
            if (originalWidth > originalHeight) {
                displayWidth = Math.min(originalWidth, containerMaxWidth);
                displayHeight = displayWidth / aspectRatio;
                if (displayHeight > containerMaxHeight) {
                    displayHeight = containerMaxHeight;
                    displayWidth = displayHeight * aspectRatio;
                }
            } else {
                displayHeight = Math.min(originalHeight, containerMaxHeight);
                displayWidth = displayHeight * aspectRatio;
                if (displayWidth > containerMaxWidth) {
                    displayWidth = containerMaxWidth;
                    displayHeight = displayWidth / aspectRatio;
                }
            }
            
            // Apply zoom to the base display size
            const zoomedWidth = displayWidth * zoomLevel;
            const zoomedHeight = displayHeight * zoomLevel;
            
            // Set the new dimensions (this will crop if zoom > 1.0)
            img.style.width = zoomedWidth + 'px';
            img.style.height = zoomedHeight + 'px';
            img.style.maxWidth = containerMaxWidth + 'px';
            img.style.maxHeight = containerMaxHeight + 'px';
            img.style.objectFit = 'cover';
            
            // Remove any scale transform
            const currentTransform = img.style.transform || '';
            const scaleRegex = /scale\([^)]*\)/g;
            const otherTransforms = currentTransform.replace(scaleRegex, '').trim();
            img.style.transform = otherTransforms;
        }
    } else {
        // Free zoom: use transform scale (original behavior)
        const currentTransform = img.style.transform || '';
        const scaleRegex = /scale\([^)]*\)/g;
        const otherTransforms = currentTransform.replace(scaleRegex, '').trim();
        
        const newTransform = `${otherTransforms} scale(${zoomLevel})`.trim();
        img.style.transform = newTransform;
        
        // Reset any constrained zoom styles
        img.style.width = '';
        img.style.height = '';
        img.style.objectFit = '';
    }
    
    // Update canvas size to match zoomed image
    updateCanvasSize(imageNum);
}

function updateCanvasSize(imageNum) {
    setTimeout(() => {
        const img = document.getElementById(`preview${imageNum}`);
        const canvas = document.getElementById(`canvas${imageNum}`);
        
        if (img && canvas) {
            // Get the actual displayed dimensions after zoom
            const rect = img.getBoundingClientRect();
            canvas.width = rect.width;
            canvas.height = rect.height;
            canvas.style.width = rect.width + 'px';
            canvas.style.height = rect.height + 'px';
            
            // Redraw masks after canvas resize
            redrawMasks(imageNum);
        }
    }, 50); // Small delay to allow transform to take effect
}

function updateZoomIndicators() {
    // Update zoom level display for visible images
    updateZoomIndicator(1);
    updateZoomIndicator(2);
}

function updateZoomIndicator(imageNum) {
    const container = document.getElementById(`canvas-container-${imageNum}`);
    if (!container || !container.classList.contains('active')) {
        return;
    }
    
    const zoomLevel = zoomLevels[imageNum];
    let indicator = container.querySelector('.zoom-indicator');
    
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.className = 'zoom-indicator';
        container.appendChild(indicator);
    }
    
    indicator.textContent = `${Math.round(zoomLevel * 100)}%`;
    
    // Auto-hide after 2 seconds
    indicator.classList.add('visible');
    setTimeout(() => {
        indicator.classList.remove('visible');
    }, 2000);
}

// Toggle zoom mode between free and constrained
function toggleZoomMode(imageNum) {
    constrainedZoomMode[imageNum] = !constrainedZoomMode[imageNum];
    const isConstrained = constrainedZoomMode[imageNum];
    
    // Update button text and appearance
    const button = document.getElementById(`zoom-mode-toggle-${imageNum}`);
    if (button) {
        if (isConstrained) {
            button.textContent = '🔓 Free Zoom';
            button.classList.add('active');
        } else {
            button.textContent = '📏 Constrained Zoom';
            button.classList.remove('active');
        }
    }
    
    // Reapply current zoom level with new mode
    const img = document.getElementById(`preview${imageNum}`);
    if (img) {
        applyZoom(img, imageNum, zoomLevels[imageNum]);
    }
    
    console.log(`Image ${imageNum} zoom mode: ${isConstrained ? 'Constrained' : 'Free'}`);
}

// Reset zoom when new image is loaded
function resetZoom(imageNum) {
    zoomLevels[imageNum] = 1.0;
    constrainedZoomMode[imageNum] = false;
    
    const img = document.getElementById(`preview${imageNum}`);
    if (img) {
        // Remove scale transform while preserving other transforms
        const currentTransform = img.style.transform || '';
        const scaleRegex = /scale\([^)]*\)/g;
        const otherTransforms = currentTransform.replace(scaleRegex, '').trim();
        img.style.transform = otherTransforms;
        
        // Reset constrained zoom styles
        img.style.width = '';
        img.style.height = '';
        img.style.objectFit = '';
    }
    
    // Reset zoom mode button
    const button = document.getElementById(`zoom-mode-toggle-${imageNum}`);
    if (button) {
        button.textContent = '📏 Constrained Zoom';
        button.classList.remove('active');
    }
}

// Expose functions globally for use by other modules
window.resetZoom = resetZoom;
window.toggleZoomMode = toggleZoomMode;