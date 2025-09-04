/**
 * Mask State Management
 * Handles global state for masks, positions, and interaction states
 */

// Store current positions for each mask (for dragging)
let maskPositions1 = {};
let maskPositions2 = {};

// Drag state
let isDragging = false;
let draggedMask = null;
let draggedImageNum = null;
let dragStartX = 0;
let dragStartY = 0;
let dragOriginalX = 0;
let dragOriginalY = 0;

// Resize state
let isResizing = false;
let resizedMask = null;
let resizedImageNum = null;
let resizeHandle = null; // 'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'
let resizeStartX = 0;
let resizeStartY = 0;
let resizeOriginalBounds = {};

// Track active masks for each image
let activeMasks1 = new Set();
let activeMasks2 = new Set();
let canvas1, canvas2, img1, img2;