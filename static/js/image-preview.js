/**
 * Image Preview and Canvas Initialization
 * Handles image uploading, preview, and canvas setup
 */

// Initialize canvas when images are loaded
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('image1').addEventListener('change', function(e) {
        previewImage(e.target, 'preview1', 'canvas1', 'canvas-container-1', 1);
    });

    document.getElementById('image2').addEventListener('change', function(e) {
        previewImage(e.target, 'preview2', 'canvas2', 'canvas-container-2', 2);
    });
});

function previewImage(input, previewId, canvasId, containerId, imageNum) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            const container = document.getElementById(containerId);
            const canvas = document.getElementById(canvasId);
            
            preview.src = e.target.result;
            preview.onload = function() {
                container.style.display = 'block';
                container.classList.add('active');
                
                // Wait a moment for image to fully render
                setTimeout(() => {
                    // Get actual displayed dimensions
                    const displayWidth = preview.offsetWidth;
                    const displayHeight = preview.offsetHeight;
                    
                    // Setup canvas to exactly match displayed image
                    canvas.width = displayWidth;
                    canvas.height = displayHeight;
                    canvas.style.width = displayWidth + 'px';
                    canvas.style.height = displayHeight + 'px';
                    
                    // Store references
                    if (imageNum === 1) {
                        canvas1 = canvas;
                        img1 = preview;
                        // Add drag event listeners
                        canvas.addEventListener('mousedown', (e) => handleMouseDown(e, 1));
                        canvas.addEventListener('mousemove', (e) => handleMouseMove(e, 1));
                        canvas.addEventListener('mouseup', (e) => handleMouseUp(e, 1));
                        canvas.addEventListener('mouseleave', (e) => handleMouseLeave(e, 1));
                    } else {
                        canvas2 = canvas;
                        img2 = preview;
                        // Add drag event listeners
                        canvas.addEventListener('mousedown', (e) => handleMouseDown(e, 2));
                        canvas.addEventListener('mousemove', (e) => handleMouseMove(e, 2));
                        canvas.addEventListener('mouseup', (e) => handleMouseUp(e, 2));
                        canvas.addEventListener('mouseleave', (e) => handleMouseLeave(e, 2));
                    }
                    
                    // Clear any existing masks
                    const activeMasks = imageNum === 1 ? activeMasks1 : activeMasks2;
                    activeMasks.clear();
                    
                    // Clear custom positions
                    if (imageNum === 1) {
                        maskPositions1 = {};
                    } else {
                        maskPositions2 = {};
                    }
                    
                    // Update button states
                    const buttons = document.querySelectorAll(`button[data-image-id="${imageNum}"].mask-btn`);
                    buttons.forEach(btn => {
                        btn.classList.remove('active');
                    });
                    
                    redrawMasks(imageNum);
                    
                    console.log(`Image ${imageNum} - Display: ${displayWidth}x${displayHeight}`);
                }, 100);
            };
        };
        reader.readAsDataURL(input.files[0]);
    }
}