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

    // Attach event listeners to preset buttons
    const presetButtons = document.querySelectorAll('.preset-btn[data-preset]');
    presetButtons.forEach(button => {
        button.addEventListener('click', function() {
            const preset = this.dataset.preset;
            const imageId = parseInt(this.dataset.imageId);
            if (preset && imageId) {
                togglePreset(preset, imageId);
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

// Toggle preset mask combinations
function togglePreset(preset, imageId) {
    const presets = {
        'eyes': ['rect_top', 'rect_bottom'],      // Top and bottom bars to focus on eyes
        'nose': ['rect_left', 'rect_right']       // Left and right bars to focus on nose
    };
    
    if (!presets[preset]) {
        console.warn('Unknown preset:', preset);
        return;
    }
    
    const maskTypes = presets[preset];
    const activeMasks = imageId === 1 ? activeMasks1 : activeMasks2;
    const presetButton = document.querySelector(`.preset-btn[data-preset="${preset}"][data-image-id="${imageId}"]`);
    
    // Check if all masks in the preset are currently active
    const allActive = maskTypes.every(maskType => activeMasks.has(maskType));
    
    if (allActive) {
        // If all are active, turn them all off
        maskTypes.forEach(maskType => {
            if (activeMasks.has(maskType)) {
                toggleMask(maskType, imageId);
            }
        });
        presetButton.classList.remove('active');
    } else {
        // If not all are active, turn them all on
        maskTypes.forEach(maskType => {
            if (!activeMasks.has(maskType)) {
                toggleMask(maskType, imageId);
            }
        });
        presetButton.classList.add('active');
    }
    
    // Update individual button states to reflect the preset change
    updatePresetButtonStates(imageId);
}

// Update preset button states based on current mask state
function updatePresetButtonStates(imageId) {
    const activeMasks = imageId === 1 ? activeMasks1 : activeMasks2;
    
    // Check eyes preset (top + bottom)
    const eyesButton = document.querySelector(`.preset-btn[data-preset="eyes"][data-image-id="${imageId}"]`);
    if (eyesButton) {
        const eyesActive = activeMasks.has('rect_top') && activeMasks.has('rect_bottom');
        eyesButton.classList.toggle('active', eyesActive);
    }
    
    // Check nose preset (left + right)
    const noseButton = document.querySelector(`.preset-btn[data-preset="nose"][data-image-id="${imageId}"]`);
    if (noseButton) {
        const noseActive = activeMasks.has('rect_left') && activeMasks.has('rect_right');
        noseButton.classList.toggle('active', noseActive);
    }
}