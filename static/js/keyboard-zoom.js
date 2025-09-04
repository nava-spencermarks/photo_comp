/**
 * Keyboard Zoom Controls
 * Handles + and - key presses to zoom images in and out
 */

// Zoom state tracking
let zoomLevels = {
    1: 1.0,  // Image 1 zoom level
    2: 1.0   // Image 2 zoom level
};

const MIN_ZOOM = 0.5;
const MAX_ZOOM = 3.0;
const ZOOM_STEP = 0.1;

document.addEventListener('DOMContentLoaded', function() {
    // Add keyboard event listener
    document.addEventListener('keydown', handleKeyboardZoom);
    
    console.log('Keyboard zoom controls initialized');
    console.log('Use + (or =) to zoom in, - to zoom out');
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
    
    // Apply zoom transform while preserving any existing transforms (like rotation)
    const currentTransform = img.style.transform || '';
    const scaleRegex = /scale\([^)]*\)/g;
    const otherTransforms = currentTransform.replace(scaleRegex, '').trim();
    
    const newTransform = `${otherTransforms} scale(${zoomLevel})`.trim();
    img.style.transform = newTransform;
    
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

// Reset zoom when new image is loaded
function resetZoom(imageNum) {
    zoomLevels[imageNum] = 1.0;
    const img = document.getElementById(`preview${imageNum}`);
    if (img) {
        // Remove scale transform while preserving other transforms
        const currentTransform = img.style.transform || '';
        const scaleRegex = /scale\([^)]*\)/g;
        const otherTransforms = currentTransform.replace(scaleRegex, '').trim();
        img.style.transform = otherTransforms;
    }
}

// Expose functions globally for use by other modules
window.resetZoom = resetZoom;