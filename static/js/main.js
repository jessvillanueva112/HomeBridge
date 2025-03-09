document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Check for browser speech API support
    if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
        const voiceBtn = document.getElementById('voice-btn');
        if (voiceBtn) {
            voiceBtn.disabled = true;
            
            // Add warning message
            const warningDiv = document.createElement('div');
            warningDiv.className = 'alert alert-warning mt-3';
            warningDiv.innerHTML = `
                <i class="fas fa-exclamation-triangle me-2"></i>
                Your browser doesn't support voice recognition. 
                Please use Chrome, Edge, or Safari for the full experience.
            `;
            
            voiceBtn.parentNode.parentNode.appendChild(warningDiv);
        }
    }
    
    // Page transitions
    document.body.classList.add('fade-in');
    
    // Dynamic year in footer
    const yearSpan = document.querySelector('.copyright-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
});
