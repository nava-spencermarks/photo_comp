/**
 * Mask Utility Functions
 * Helper functions for mask detection, cursor handling, etc.
 */

// Helper function to get mask at position
function getMaskAtPosition(x, y, imageNum) {
    const canvas = imageNum === 1 ? canvas1 : canvas2;
    const activeMasks = imageNum === 1 ? activeMasks1 : activeMasks2;
    const positions = imageNum === 1 ? maskPositions1 : maskPositions2;
    
    // Check each active mask to see if click is inside it
    for (let maskType of activeMasks) {
        const pos = positions[maskType] || RECTANGLE_PATTERNS[maskType];
        const maskX = pos.x * canvas.width;
        const maskY = pos.y * canvas.height;
        const maskWidth = pos.width * canvas.width;
        const maskHeight = pos.height * canvas.height;
        
        if (x >= maskX && x <= maskX + maskWidth && 
            y >= maskY && y <= maskY + maskHeight) {
            return maskType;
        }
    }
    return null;
}

// Helper function to detect resize handle
function getResizeHandle(x, y, maskType, imageNum) {
    const canvas = imageNum === 1 ? canvas1 : canvas2;
    const positions = imageNum === 1 ? maskPositions1 : maskPositions2;
    const pos = positions[maskType] || RECTANGLE_PATTERNS[maskType];
    
    const maskX = pos.x * canvas.width;
    const maskY = pos.y * canvas.height;
    const maskWidth = pos.width * canvas.width;
    const maskHeight = pos.height * canvas.height;
    
    const left = maskX;
    const right = maskX + maskWidth;
    const top = maskY;
    const bottom = maskY + maskHeight;
    
    // Check corners first (they take priority)
    if (Math.abs(x - left) <= RESIZE_HANDLE_SIZE && Math.abs(y - top) <= RESIZE_HANDLE_SIZE) {
        return 'nw';
    }
    if (Math.abs(x - right) <= RESIZE_HANDLE_SIZE && Math.abs(y - top) <= RESIZE_HANDLE_SIZE) {
        return 'ne';
    }
    if (Math.abs(x - left) <= RESIZE_HANDLE_SIZE && Math.abs(y - bottom) <= RESIZE_HANDLE_SIZE) {
        return 'sw';
    }
    if (Math.abs(x - right) <= RESIZE_HANDLE_SIZE && Math.abs(y - bottom) <= RESIZE_HANDLE_SIZE) {
        return 'se';
    }
    
    // Check edges
    if (Math.abs(x - left) <= RESIZE_HANDLE_SIZE && y >= top && y <= bottom) {
        return 'w';
    }
    if (Math.abs(x - right) <= RESIZE_HANDLE_SIZE && y >= top && y <= bottom) {
        return 'e';
    }
    if (Math.abs(y - top) <= RESIZE_HANDLE_SIZE && x >= left && x <= right) {
        return 'n';
    }
    if (Math.abs(y - bottom) <= RESIZE_HANDLE_SIZE && x >= left && x <= right) {
        return 's';
    }
    
    return null;
}

// Helper function to get cursor style for resize handle
function getResizeCursor(handle) {
    const cursors = {
        'n': 'ns-resize',
        's': 'ns-resize',
        'e': 'ew-resize',
        'w': 'ew-resize',
        'ne': 'nesw-resize',
        'nw': 'nwse-resize',
        'se': 'nwse-resize',
        'sw': 'nesw-resize'
    };
    return cursors[handle] || 'default';
}