// Button click handlers for mask operations

document.addEventListener('DOMContentLoaded', function() {
    // Attach event listeners to all mask buttons
    const maskButtons = document.querySelectorAll('.mask-btn[data-mask-type]');
    maskButtons.forEach(button => {
        button.addEventListener('click', function() {
            const maskType = this.dataset.maskType;
            const imageId = parseInt(this.dataset.imageId);
            if (maskType && imageId) {
                toggleMask(maskType, imageId);
            }
        });
    });

    // Clear all masks buttons
    const clearButtons = document.querySelectorAll('.btn-clear-masks');
    clearButtons.forEach(button => {
        button.addEventListener('click', function() {
            const imageId = parseInt(this.dataset.imageId);
            if (imageId) {
                clearAllMasks(imageId);
            }
        });
    });

    // Flip image buttons
    const flipButtons = document.querySelectorAll('.btn-flip-image');
    flipButtons.forEach(button => {
        button.addEventListener('click', function() {
            const previewId = this.dataset.previewId;
            if (previewId) {
                flipImage(previewId);
            }
        });
    });
});