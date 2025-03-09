/**
 * Main application JavaScript file
 * Handles general application functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle voice recording buttons
    const startRecordingBtn = document.getElementById('start-recording-btn');
    const stopRecordingBtn = document.getElementById('stop-recording-btn');
    const processRecordingBtn = document.getElementById('process-recording-btn');

    if (startRecordingBtn) {
        startRecordingBtn.addEventListener('click', function() {
            voiceInteraction.startListening();
        });
    }

    if (stopRecordingBtn) {
        stopRecordingBtn.addEventListener('click', function() {
            voiceInteraction.stopListening();
        });
    }

    if (processRecordingBtn) {
        processRecordingBtn.addEventListener('click', function() {
            voiceInteraction.processVoiceInput();
        });
    }

    // Handle the dismiss button for error alerts
    const dismissBtns = document.querySelectorAll('.btn-close[data-bs-dismiss="alert"]');
    dismissBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.classList.add('d-none');
            }
        });
    });

    // Handle resource category buttons
    const resourceCategoryBtns = document.querySelectorAll('.resource-category-btn');
    resourceCategoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            
            // Hide all resource sections
            document.querySelectorAll('.resource-section').forEach(section => {
                section.classList.add('d-none');
            });
            
            // Show the selected category
            const selectedSection = document.getElementById(`${category}-resources`);
            if (selectedSection) {
                selectedSection.classList.remove('d-none');
            }
            
            // Update active button state
            resourceCategoryBtns.forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
        });
    });

    // Gratitude practice modal handling
    const gratitudeForm = document.getElementById('gratitude-form');
    if (gratitudeForm) {
        gratitudeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const gratitudeInput = document.getElementById('gratitude-input');
            if (gratitudeInput && gratitudeInput.value.trim() !== '') {
                // Show success message
                const gratitudeModal = bootstrap.Modal.getInstance(document.getElementById('gratitudeModal'));
                gratitudeModal.hide();
                
                // Show success toast
                const toast = new bootstrap.Toast(document.getElementById('gratitude-toast'));
                toast.show();
                
                // Clear input
                gratitudeInput.value = '';
            }
        });
    }

    // Progress tracker functionality
    const progressItems = document.querySelectorAll('.progress-item');
    if (progressItems.length > 0) {
        progressItems.forEach(item => {
            const checkbox = item.querySelector('input[type="checkbox"]');
            checkbox.addEventListener('change', function() {
                // Update the progress item's appearance
                if (this.checked) {
                    item.classList.add('completed');
                } else {
                    item.classList.remove('completed');
                }
                
                // Update the progress bar
                updateProgressBar();
            });
        });

        // Initial progress bar update
        updateProgressBar();
    }

    // Function to update the progress bar
    function updateProgressBar() {
        const totalItems = document.querySelectorAll('.progress-item').length;
        const completedItems = document.querySelectorAll('.progress-item.completed').length;
        
        if (totalItems > 0) {
            const progressPercentage = (completedItems / totalItems) * 100;
            const progressBar = document.querySelector('.progress-bar');
            if (progressBar) {
                progressBar.style.width = progressPercentage + '%';
                progressBar.setAttribute('aria-valuenow', progressPercentage);
                progressBar.textContent = Math.round(progressPercentage) + '%';
            }
        }
    }
});

// Handle page transitions with a simple fade effect
document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('page-loaded');
});
