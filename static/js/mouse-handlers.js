/**
 * Mouse Event Handlers
 * Handles mouse interactions for dragging and resizing masks
 */

// Mouse event handlers for dragging and resizing
function handleMouseDown(e, imageNum) {
    const canvas = imageNum === 1 ? canvas1 : canvas2;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const mask = getMaskAtPosition(x, y, imageNum);
    if (mask) {
        const handle = getResizeHandle(x, y, mask, imageNum);
        
        if (handle) {
            // Start resizing
            isResizing = true;
            resizedMask = mask;
            resizedImageNum = imageNum;
            resizeHandle = handle;
            resizeStartX = x;
            resizeStartY = y;
            
            const positions = imageNum === 1 ? maskPositions1 : maskPositions2;
            const currentPos = positions[mask] || RECTANGLE_PATTERNS[mask];
            resizeOriginalBounds = {
                x: currentPos.x * canvas.width,
                y: currentPos.y * canvas.height,
                width: currentPos.width * canvas.width,
                height: currentPos.height * canvas.height
            };
            
            canvas.style.cursor = getResizeCursor(handle);
        } else {
            // Start dragging
            isDragging = true;
            draggedMask = mask;
            draggedImageNum = imageNum;
            dragStartX = x;
            dragStartY = y;
            
            const positions = imageNum === 1 ? maskPositions1 : maskPositions2;
            const currentPos = positions[mask] || RECTANGLE_PATTERNS[mask];
            dragOriginalX = currentPos.x * canvas.width;
            dragOriginalY = currentPos.y * canvas.height;
            
            canvas.style.cursor = 'grabbing';
        }
        e.preventDefault();
    }
}

function handleMouseMove(e, imageNum) {
    const canvas = imageNum === 1 ? canvas1 : canvas2;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    if (isResizing && resizedImageNum === imageNum) {
        // Handle resizing
        const deltaX = x - resizeStartX;
        const deltaY = y - resizeStartY;
        
        let newX = resizeOriginalBounds.x / canvas.width;
        let newY = resizeOriginalBounds.y / canvas.height;
        let newWidth = resizeOriginalBounds.width / canvas.width;
        let newHeight = resizeOriginalBounds.height / canvas.height;
        
        // Update dimensions based on resize handle
        if (resizeHandle.includes('w')) {
            const newLeft = (resizeOriginalBounds.x + deltaX) / canvas.width;
            const newRight = (resizeOriginalBounds.x + resizeOriginalBounds.width) / canvas.width;
            if (newLeft < newRight) {
                newX = newLeft;
                newWidth = newRight - newLeft;
            }
        }
        if (resizeHandle.includes('e')) {
            newWidth = (resizeOriginalBounds.width + deltaX) / canvas.width;
            if (newWidth < 0.05) newWidth = 0.05; // Minimum width
        }
        if (resizeHandle.includes('n')) {
            const newTop = (resizeOriginalBounds.y + deltaY) / canvas.height;
            const newBottom = (resizeOriginalBounds.y + resizeOriginalBounds.height) / canvas.height;
            if (newTop < newBottom) {
                newY = newTop;
                newHeight = newBottom - newTop;
            }
        }
        if (resizeHandle.includes('s')) {
            newHeight = (resizeOriginalBounds.height + deltaY) / canvas.height;
            if (newHeight < 0.05) newHeight = 0.05; // Minimum height
        }
        
        // Update positions for both images (synchronized)
        maskPositions1[resizedMask] = {
            x: newX,
            y: newY,
            width: newWidth,
            height: newHeight
        };
        maskPositions2[resizedMask] = {
            x: newX,
            y: newY,
            width: newWidth,
            height: newHeight
        };
        
        // Redraw both canvases
        redrawMasks(1);
        redrawMasks(2);
        
    } else if (isDragging && draggedImageNum === imageNum) {
        // Calculate new position for dragging
        const deltaX = x - dragStartX;
        const deltaY = y - dragStartY;
        const newX = (dragOriginalX + deltaX) / canvas.width;
        const newY = (dragOriginalY + deltaY) / canvas.height;
        
        // Get current dimensions
        const positions = imageNum === 1 ? maskPositions1 : maskPositions2;
        const currentPos = positions[draggedMask] || RECTANGLE_PATTERNS[draggedMask];
        
        // Update position for both images (to keep them synchronized)
        maskPositions1[draggedMask] = {
            x: newX,
            y: newY,
            width: currentPos.width,
            height: currentPos.height
        };
        maskPositions2[draggedMask] = {
            x: newX,
            y: newY,
            width: currentPos.width,
            height: currentPos.height
        };
        
        // Redraw both canvases
        redrawMasks(1);
        redrawMasks(2);
    } else if (!isDragging && !isResizing) {
        // Update cursor based on hover
        const mask = getMaskAtPosition(x, y, imageNum);
        if (mask) {
            const handle = getResizeHandle(x, y, mask, imageNum);
            if (handle) {
                canvas.style.cursor = getResizeCursor(handle);
            } else {
                canvas.style.cursor = 'grab';
            }
        } else {
            canvas.style.cursor = 'default';
        }
    }
}

function handleMouseUp(e, imageNum) {
    if (isDragging) {
        isDragging = false;
        draggedMask = null;
        draggedImageNum = null;
        
        const canvas = imageNum === 1 ? canvas1 : canvas2;
        canvas.style.cursor = 'move';
    }
    
    if (isResizing) {
        isResizing = false;
        resizedMask = null;
        resizedImageNum = null;
        resizeHandle = null;
        
        const canvas = imageNum === 1 ? canvas1 : canvas2;
        canvas.style.cursor = 'move';
    }
}

function handleMouseLeave(e, imageNum) {
    if ((isDragging && draggedImageNum === imageNum) || 
        (isResizing && resizedImageNum === imageNum)) {
        handleMouseUp(e, imageNum);
    }
}