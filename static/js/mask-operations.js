/**
 * Mask Operations
 * Functions for managing mask toggles, clearing, and canvas drawing
 */

// Image flip functionality
function flipImage(imageId) {
    const img = document.getElementById(imageId);
    const currentTransform = img.style.transform || '';
    
    if (currentTransform.includes('rotate(180deg)')) {
        img.style.transform = currentTransform.replace('rotate(180deg)', '').trim();
    } else {
        img.style.transform = (currentTransform + ' rotate(180deg)').trim();
    }
}

// Toggle mask for specific area - sync both images
function toggleMask(maskType, imageNum) {
    // Update both mask sets to stay synchronized
    if (activeMasks1.has(maskType)) {
        activeMasks1.delete(maskType);
        activeMasks2.delete(maskType);
        // Remove custom positions when mask is removed
        delete maskPositions1[maskType];
        delete maskPositions2[maskType];
    } else {
        activeMasks1.add(maskType);
        activeMasks2.add(maskType);
        // Initialize with default positions
        maskPositions1[maskType] = {...RECTANGLE_PATTERNS[maskType]};
        maskPositions2[maskType] = {...RECTANGLE_PATTERNS[maskType]};
    }
    
    // Update ALL button appearances (both image sets)
    const allButtons = document.querySelectorAll(`button[data-mask-type="${maskType}"].mask-btn`);
    allButtons.forEach(btn => {
        if (activeMasks1.has(maskType)) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Update preset button states
    updatePresetButtonStates(1);
    updatePresetButtonStates(2);
    
    // Redraw masks on both images
    redrawMasks(1);
    redrawMasks(2);
    
    console.log(`Toggled ${maskType}. Active masks:`, Array.from(activeMasks1));
}

// Clear all masks - sync both images
function clearAllMasks(imageNum) {
    // Clear both mask sets to stay synchronized
    activeMasks1.clear();
    activeMasks2.clear();
    
    // Clear custom positions
    maskPositions1 = {};
    maskPositions2 = {};
    
    // Update ALL button appearances
    const allButtons = document.querySelectorAll('.mask-btn');
    allButtons.forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Update preset button states
    const allPresetButtons = document.querySelectorAll('.preset-btn');
    allPresetButtons.forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Redraw masks on both images
    redrawMasks(1);
    redrawMasks(2);
    
    console.log('Cleared all masks');
}

// Redraw masks on canvas
function redrawMasks(imageNum) {
    const canvas = imageNum === 1 ? canvas1 : canvas2;
    const img = imageNum === 1 ? img1 : img2;
    const activeMasks = imageNum === 1 ? activeMasks1 : activeMasks2;
    const positions = imageNum === 1 ? maskPositions1 : maskPositions2;
    
    if (!canvas || !img || !canvas.getContext) {
        console.log(`Cannot redraw masks for image ${imageNum} - missing canvas or image`);
        return;
    }
    
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    console.log(`Redrawing masks for image ${imageNum}. Canvas size: ${canvas.width}x${canvas.height}. Active masks:`, Array.from(activeMasks));
    
    // Draw each active mask
    activeMasks.forEach(maskType => {
        // Use custom position if available, otherwise use default
        const maskDef = positions[maskType] || RECTANGLE_PATTERNS[maskType];
        if (maskDef) {
            const x = Math.round(maskDef.x * canvas.width);
            const y = Math.round(maskDef.y * canvas.height);
            const width = Math.round(maskDef.width * canvas.width);
            const height = Math.round(maskDef.height * canvas.height);
            
            console.log(`Drawing ${maskType} mask at (${x}, ${y}) size ${width}x${height}`);
            
            ctx.fillStyle = '#555555';
            ctx.fillRect(x, y, width, height);
            
            // Add border when being dragged or resized for better visual feedback
            if ((isDragging && draggedMask === maskType) || 
                (isResizing && resizedMask === maskType)) {
                ctx.strokeStyle = '#ff0000';
                ctx.lineWidth = 2;
                ctx.strokeRect(x, y, width, height);
                
                // Draw resize handles when resizing
                if (isResizing && resizedMask === maskType) {
                    ctx.fillStyle = '#ffffff';
                    ctx.strokeStyle = '#ff0000';
                    ctx.lineWidth = 1;
                    
                    // Corner handles
                    const handleSize = 6;
                    const handles = [
                        [x - handleSize/2, y - handleSize/2],  // nw
                        [x + width - handleSize/2, y - handleSize/2],  // ne
                        [x - handleSize/2, y + height - handleSize/2],  // sw
                        [x + width - handleSize/2, y + height - handleSize/2],  // se
                        [x + width/2 - handleSize/2, y - handleSize/2],  // n
                        [x + width/2 - handleSize/2, y + height - handleSize/2],  // s
                        [x - handleSize/2, y + height/2 - handleSize/2],  // w
                        [x + width - handleSize/2, y + height/2 - handleSize/2]  // e
                    ];
                    
                    handles.forEach(([hx, hy]) => {
                        ctx.fillRect(hx, hy, handleSize, handleSize);
                        ctx.strokeRect(hx, hy, handleSize, handleSize);
                    });
                }
            }
        }
    });
}