/**
 * Rectangle Patterns Configuration
 * Defines the default mask patterns and constants
 */

// Rectangle patterns - masks that extend to edges like in correct.png
const RECTANGLE_PATTERNS = {
    // Horizontal rectangles that span full width
    rect_top: { x: 0, y: 0, width: 1.0, height: 0.35 },           // Top horizontal bar
    rect_middle: { x: 0, y: 0.35, width: 1.0, height: 0.30 },     // Middle horizontal bar
    rect_bottom: { x: 0, y: 0.65, width: 1.0, height: 0.35 },     // Bottom horizontal bar
    
    // Vertical rectangles that span full height
    rect_left: { x: 0, y: 0, width: 0.35, height: 1.0 },          // Left vertical bar
    rect_right: { x: 0.65, y: 0, width: 0.35, height: 1.0 },      // Right vertical bar
    
    // Center pattern
    rect_center: { x: 0.30, y: 0.30, width: 0.40, height: 0.40 }  // Center square
};

// Configuration constants
const RESIZE_HANDLE_SIZE = 8; // pixels for resize handle detection