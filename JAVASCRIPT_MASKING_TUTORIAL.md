# JavaScript Image Masking System Tutorial

## Overview
This system creates rectangular masks over uploaded images using HTML5 Canvas overlays. Think of it as creating digital "post-it notes" that can be placed over facial features for comparison purposes.

## Core Concepts

### 1. HTML Structure
```html
<div class="image-canvas-container" style="position: relative;">
    <img id="preview1" style="max-width: 300px; max-height: 300px;">
    <canvas id="canvas1" style="position: absolute; top: 0; left: 0;"></canvas>
</div>
```

**Key Points:**
- Container uses `position: relative` (like CSS `position: relative`)
- Image is the base layer
- Canvas is positioned absolutely on top (`position: absolute`)
- Canvas acts like a transparent overlay where we draw rectangles

### 2. Coordinate System
```javascript
const RECTANGLE_PATTERNS = {
    rect_top: { x: 0.15, y: 0.10, width: 0.70, height: 0.25 }
};
```

**Coordinate System Explanation:**
- Uses **percentage-based coordinates** (0.0 to 1.0)
- `x: 0.15` = 15% from left edge
- `y: 0.10` = 10% from top edge  
- `width: 0.70` = 70% of image width
- `height: 0.25` = 25% of image height

**Why Percentages?** Images can be different sizes, but facial proportions remain consistent.

### 3. State Management
```javascript
let activeMasks1 = new Set();  // Tracks which masks are active for image 1
let activeMasks2 = new Set();  // Tracks which masks are active for image 2
let canvas1, canvas2, img1, img2;  // References to DOM elements
```

**JavaScript Sets:**
- Like a HashSet - stores unique values
- `activeMasks1.add('rect_top')` - adds a mask
- `activeMasks1.has('rect_top')` - checks if mask exists
- `activeMasks1.delete('rect_top')` - removes a mask

## Core Functions Explained

### 1. Image Upload & Canvas Setup
```javascript
function previewImage(input, previewId, canvasId, containerId, imageNum) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            const container = document.getElementById(containerId);
            const canvas = document.getElementById(canvasId);
            
            preview.src = e.target.result;  // Set image source
            preview.onload = function() {   // Wait for image to load
                // ... setup canvas
            };
        };
        reader.readAsDataURL(input.files[0]);  // Convert file to base64
    }
}
```

**Flow:**
1. User selects file via `<input type="file">`
2. `FileReader` converts file to base64 data URL (like: `data:image/png;base64,iVBOR...`)
3. Set image `src` to this data URL
4. Wait for image to fully load before setting up canvas

**Canvas Setup (Critical Part):**
```javascript
setTimeout(() => {
    // Get actual displayed dimensions
    const displayWidth = preview.offsetWidth;   // Actual displayed width
    const displayHeight = preview.offsetHeight; // Actual displayed height
    
    // Make canvas exactly match image size
    canvas.width = displayWidth;
    canvas.height = displayHeight;
    canvas.style.width = displayWidth + 'px';
    canvas.style.height = displayHeight + 'px';
    canvas.style.position = 'absolute';
    canvas.style.top = '0px';
    canvas.style.left = '0px';
}, 100);
```

**Why setTimeout?** Images don't instantly appear - we need to wait for browser layout to complete.

### 2. Toggle Mask Function
```javascript
function toggleMask(maskType, imageNum) {
    // Update BOTH mask sets to stay synchronized
    if (activeMasks1.has(maskType)) {
        activeMasks1.delete(maskType);
        activeMasks2.delete(maskType);
    } else {
        activeMasks1.add(maskType);
        activeMasks2.add(maskType);
    }
    
    // Update ALL button appearances
    const allButtons = document.querySelectorAll(`button[onclick*="toggleMask('${maskType}',"]`);
    allButtons.forEach(btn => {
        if (activeMasks1.has(maskType)) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Redraw masks on both images
    redrawMasks(1);
    redrawMasks(2);
}
```

**Key Behaviors:**
- **Synchronization:** Both images always show identical masks
- **Button Updates:** All buttons with same mask type get updated appearance
- **Immediate Redraw:** Canvas is redrawn after every change

### 3. Canvas Drawing Function
```javascript
function redrawMasks(imageNum) {
    const canvas = imageNum === 1 ? canvas1 : canvas2;
    const activeMasks = imageNum === 1 ? activeMasks1 : activeMasks2;
    
    const ctx = canvas.getContext('2d');  // Get drawing context
    ctx.clearRect(0, 0, canvas.width, canvas.height);  // Clear everything
    
    // Draw each active mask
    activeMasks.forEach(maskType => {
        const maskDef = RECTANGLE_PATTERNS[maskType];
        if (maskDef) {
            // Convert percentages to pixels
            const x = Math.round(maskDef.x * canvas.width);
            const y = Math.round(maskDef.y * canvas.height);
            const width = Math.round(maskDef.width * canvas.width);
            const height = Math.round(maskDef.height * canvas.height);
            
            // Draw rectangle
            ctx.fillStyle = '#555555';  // Dark gray
            ctx.fillRect(x, y, width, height);
        }
    });
}
```

**Canvas 2D Context:**
- `getContext('2d')` - Gets drawing API (like getting a Graphics object)
- `clearRect()` - Erases rectangular area (we clear entire canvas)
- `fillStyle` - Sets fill color
- `fillRect(x, y, width, height)` - Draws filled rectangle

**Coordinate Conversion:**
- `maskDef.x * canvas.width` converts 0.15 → actual pixels
- `Math.round()` ensures whole pixel values

## Event Handling

### Button Click Events
```html
<button onclick="toggleMask('rect_top', 1)">Top Bar</button>
```

**How onclick Works:**
- When clicked, calls `toggleMask('rect_top', 1)`
- Function receives mask type and image number
- Updates state and redraws canvas

### File Input Events
```javascript
document.getElementById('image1').addEventListener('change', function(e) {
    previewImage(e.target, 'preview1', 'canvas1', 'canvas-container-1', 1);
});
```

**Event Listener Pattern:**
- `addEventListener('change', function)` - Like attaching event handler
- `e.target` - The file input element that triggered event
- Calls preview function with specific element IDs

### Form Submission
```javascript
document.querySelector('form').addEventListener('submit', function(e) {
    // Convert active masks to data for backend
    const rects1 = Array.from(activeMasks1).map(maskType => {
        const mask = RECTANGLE_PATTERNS[maskType];
        return {
            x: mask.x,
            y: mask.y,
            width: mask.width,
            height: mask.height
        };
    });
    
    // Add hidden inputs to form
    const input1 = document.createElement('input');
    input1.type = 'hidden';
    input1.name = 'rectangles1';
    input1.value = JSON.stringify(rects1);
    this.appendChild(input1);
});
```

**Form Data Preparation:**
- Convert Set to Array: `Array.from(activeMasks1)`
- Map each mask type to coordinates: `.map(maskType => ...)`
- Create hidden form inputs dynamically
- Serialize as JSON for backend

## Common Debugging Issues

### 1. Canvas Not Aligned with Image
**Problem:** Rectangles appear in wrong position
**Cause:** Canvas size doesn't match displayed image size
**Fix:** Ensure `canvas.width = preview.offsetWidth`

### 2. Masks Disappear on Redraw
**Problem:** Masks vanish when toggling
**Cause:** Canvas wasn't cleared and redrawn properly
**Fix:** Always `clearRect()` before redrawing all active masks

### 3. Button States Out of Sync
**Problem:** Button appearance doesn't match active masks
**Cause:** Not updating all buttons when mask state changes
**Fix:** Use `querySelectorAll()` to find all relevant buttons

### 4. Coordinate System Confusion
**Problem:** Rectangles in wrong locations
**Cause:** Mixing pixel coordinates with percentage coordinates
**Fix:** Always convert: `percentage * canvas.dimension`

## Architecture Benefits

### 1. Separation of Concerns
- **HTML:** Structure and layout
- **CSS:** Styling and positioning  
- **JavaScript:** Behavior and interaction

### 2. Declarative Mask Definitions
```javascript
const RECTANGLE_PATTERNS = {
    rect_top: { x: 0.15, y: 0.10, width: 0.70, height: 0.25 }
};
```
- Masks defined as data, not code
- Easy to modify positions without changing logic
- Percentage-based for responsive design

### 3. Synchronization Pattern
- Single source of truth for mask state
- Automatic UI updates when state changes
- Both images always show identical masks

### 4. Canvas vs DOM Manipulation
**Why Canvas over DOM elements?**
- Canvas is faster for frequent redraws
- Precise pixel control
- No DOM complexity (creating/destroying elements)
- Easy to clear and redraw entire state

## JavaScript-Specific Concepts for Non-JS Developers

### 1. Asynchronous Operations (The Biggest JavaScript Gotcha)
```javascript
// This is NOT like synchronous file reading in other languages
const reader = new FileReader();
reader.onload = function(e) {
    // This code runs LATER, when file is done reading
    preview.src = e.target.result;
    preview.onload = function() {
        // This runs EVEN LATER, when image finishes loading
        setupCanvas();
    };
};
reader.readAsDataURL(input.files[0]); // This starts the process but returns immediately
// Code here runs BEFORE the file is read!
```

**Why This Matters:**
- JavaScript is single-threaded but non-blocking
- File operations, image loading, network requests are asynchronous
- You CANNOT do: `image.src = file; setupCanvas();` (setupCanvas runs before image loads)
- **Think of it like:** Starting a background thread, but using callbacks instead of `join()`

### 2. The FileReader API Deep Dive
```javascript
const reader = new FileReader();
reader.readAsDataURL(input.files[0]);
```

**What's Actually Happening:**
- `input.files[0]` is a File object (binary data)
- `readAsDataURL()` converts binary → base64 string
- Result looks like: `"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."`
- This base64 string can be used directly as `<img src="...">`

**Why Base64?** Browsers can't directly display File objects. Base64 is a text representation of binary data that browsers understand.

### 3. DOM Element Properties vs CSS Styles
```javascript
// These are DIFFERENT things:
preview.offsetWidth    // Actual rendered pixel width (read-only)
preview.style.width    // CSS width property (string like "300px")
preview.width          // HTML width attribute (number)

// For canvas sizing, you need BOTH:
canvas.width = 300;           // Sets internal canvas resolution
canvas.style.width = "300px"; // Sets displayed CSS size
```

**Common Mistake:** Setting only `canvas.style.width` makes canvas blurry (browser stretches low-res canvas).

### 4. CSS Positioning Context Explained
```html
<div style="position: relative;">     <!-- Creates positioning context -->
    <img id="image">
    <canvas style="position: absolute; top: 0; left: 0;"></canvas>
</div>
```

**How This Works:**
- Parent has `position: relative` (creates coordinate system)
- Canvas has `position: absolute` (positioned relative to parent)
- `top: 0; left: 0` means canvas starts at parent's top-left corner
- **Without relative parent:** Canvas would position relative to entire page

### 5. JavaScript Truthiness and Guards
```javascript
if (input.files && input.files[0]) {
    // Process file
}
```

**What This Checks:**
- `input.files` exists (not null/undefined)
- `input.files[0]` exists (array has at least one item)
- **In other languages:** You might check `input.files != null && input.files.length > 0`
- **JavaScript shorthand:** Relies on "falsy" values (null, undefined, empty array all evaluate to false)

### 6. Array/Collection Methods (Functional Programming Style)
```javascript
// Convert Set to Array, then transform each element
const rects = Array.from(activeMasks1).map(maskType => {
    const mask = RECTANGLE_PATTERNS[maskType];
    return { x: mask.x, y: mask.y, width: mask.width, height: mask.height };
});
```

**Step by Step:**
1. `Array.from(activeMasks1)` → `['rect_top', 'rect_middle']`
2. `.map(maskType => {...})` → Transform each string into object
3. Result: `[{x: 0.15, y: 0.10, ...}, {x: 0.20, y: 0.40, ...}]`

**Think of it like:** LINQ's `Select()` or Java 8 streams' `map()`

### 7. Event Delegation and Query Selectors
```javascript
const allButtons = document.querySelectorAll(`button[onclick*="toggleMask('${maskType}',"]`);
allButtons.forEach(btn => btn.classList.add('active'));
```

**What This Does:**
- `querySelectorAll()` uses CSS selector syntax to find elements
- `button[onclick*="toggleMask('rect_top',"]` finds buttons whose onclick contains that string
- Finds buttons for BOTH images (since they both have same mask type)
- **Alternative approach:** Could use event delegation, but inline onclick is simpler here

### 8. Callback Functions and Scope Capture
```javascript
preview.onload = function() {
    setTimeout(() => {
        const displayWidth = preview.offsetWidth; // 'preview' captured from outer scope
        setupCanvasSize(displayWidth);
    }, 100);
};
```

**Scope Capture Explained:**
- Inner function "closes over" variables from outer scope
- `preview` variable is "captured" when setTimeout function is created
- Even after outer function ends, inner function still has access to `preview`
- **Like:** Lambda captures in C# or closures in other languages

### 9. Why setTimeout(callback, 100)?
```javascript
preview.onload = function() {
    setTimeout(() => setupCanvas(), 100); // Wait 100ms
};
```

**The Problem:** Even after `img.onload` fires, browser layout might not be complete
**The Solution:** Small delay allows browser to:
- Calculate final image dimensions
- Apply CSS styles
- Complete layout reflow

**Better Alternatives:** `requestAnimationFrame()` or `ResizeObserver`, but setTimeout is simple and works.

### 10. Canvas Drawing State Machine
```javascript
const ctx = canvas.getContext('2d');
ctx.fillStyle = '#555555';  // Sets fill color for ALL future operations
ctx.fillRect(x, y, w, h);   // Uses current fillStyle
ctx.fillRect(x2, y2, w2, h2); // Still uses same fillStyle!
```

**Important:** Canvas context maintains state. Setting `fillStyle` affects all subsequent drawing operations until changed.

## Advanced Debugging Techniques for JavaScript-Haters

### 1. Console Debugging
```javascript
console.log('Canvas size:', canvas.width, 'x', canvas.height);
console.log('Image size:', preview.offsetWidth, 'x', preview.offsetHeight);
console.log('Active masks:', Array.from(activeMasks1));
```

### 2. Element Inspector
- Right-click canvas → Inspect Element
- Check `style` attribute for positioning
- Verify `width` and `height` attributes match displayed size

### 3. Common "JavaScript Is Broken" Moments
**Problem:** "My canvas setup code isn't working!"
**Reality:** Code runs before image loads (async issue)

**Problem:** "querySelector isn't finding my dynamically created elements!"
**Reality:** Query runs before elements are added to DOM

**Problem:** "Canvas is blurry even though size is correct!"
**Reality:** CSS size ≠ internal resolution. Set both `canvas.width` AND `canvas.style.width`

This masking system demonstrates common JavaScript pain points: async operations, DOM manipulation quirks, event handling, and canvas drawing - all while maintaining synchronization between multiple UI elements.