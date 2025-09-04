/**
 * Form Submission Handler
 * Handles form submission and mask data preparation
 */

// Form submission with mask data
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function(e) {
        // Convert active masks to rectangle format for backend
        const rects1 = Array.from(activeMasks1).map(maskType => {
            // Use custom position if available, otherwise use default
            const mask = maskPositions1[maskType] || RECTANGLE_PATTERNS[maskType];
            return {
                x: mask.x,
                y: mask.y, 
                width: mask.width,
                height: mask.height
            };
        });
        
        const rects2 = Array.from(activeMasks2).map(maskType => {
            // Use custom position if available, otherwise use default
            const mask = maskPositions2[maskType] || RECTANGLE_PATTERNS[maskType];
            return {
                x: mask.x,
                y: mask.y,
                width: mask.width, 
                height: mask.height
            };
        });
        
        // Add hidden inputs
        const input1 = document.createElement('input');
        input1.type = 'hidden';
        input1.name = 'rectangles1';
        input1.value = JSON.stringify(rects1);
        this.appendChild(input1);
        
        const input2 = document.createElement('input');
        input2.type = 'hidden';
        input2.name = 'rectangles2';
        input2.value = JSON.stringify(rects2);
        this.appendChild(input2);
        
        console.log('Submitting with masks - Image 1:', rects1, 'Image 2:', rects2);
    });
});