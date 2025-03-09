/**
 * Voice Interaction Module
 * Handles voice input and speech recognition for the application
 */

class VoiceInteraction {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.transcript = '';
        this.initSpeechRecognition();
    }

    /**
     * Initialize the speech recognition system
     */
    initSpeechRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.error('Speech recognition not supported in this browser');
            this.showBrowserSupportError();
            return;
        }

        // Create speech recognition object
        this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        
        // Configure
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';

        // Set up event handlers
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateUI('listening');
            console.log('Voice recognition started');
        };

        this.recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            // Update the UI with the transcript
            if (finalTranscript !== '') {
                this.transcript = finalTranscript;
                document.getElementById('transcription-text').textContent = this.transcript;
            }
            
            if (interimTranscript !== '') {
                document.getElementById('interim-text').textContent = interimTranscript;
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            this.isListening = false;
            this.updateUI('error', event.error);
        };

        this.recognition.onend = () => {
            this.isListening = false;
            this.updateUI('stopped');
            console.log('Voice recognition ended');
        };
    }

    /**
     * Start listening for voice input
     */
    startListening() {
        if (!this.recognition) {
            this.showBrowserSupportError();
            return;
        }

        if (!this.isListening) {
            // Clear previous transcript
            this.transcript = '';
            document.getElementById('transcription-text').textContent = '';
            document.getElementById('interim-text').textContent = '';
            
            try {
                this.recognition.start();
            } catch (e) {
                console.error('Error starting speech recognition:', e);
                this.updateUI('error', e.message);
            }
        }
    }

    /**
     * Stop listening for voice input
     */
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            document.getElementById('interim-text').textContent = '';
        }
    }

    /**
     * Process the voice input after stopping recording
     */
    processVoiceInput() {
        if (!this.transcript || this.transcript.trim() === '') {
            this.showError('No speech was detected. Please try again.');
            return;
        }

        this.updateUI('processing');

        // Send the transcript to the server for analysis
        fetch('/process_voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: this.transcript }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                this.showError(data.error);
                return;
            }
            
            // Handle successful processing
            this.displayResults(data);
            this.updateUI('completed');
        })
        .catch(error => {
            console.error('Error processing voice input:', error);
            this.showError('There was an error processing your input. Please try again.');
            this.updateUI('error', error.message);
        });
    }

    /**
     * Display the analysis results and strategies
     */
    displayResults(data) {
        const resultsContainer = document.getElementById('results-container');
        resultsContainer.classList.remove('d-none');
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });

        // Display strategies
        const strategiesContainer = document.getElementById('strategies-container');
        strategiesContainer.innerHTML = '';
        
        if (data.strategies && data.strategies.length > 0) {
            data.strategies.forEach(strategy => {
                const strategyCard = document.createElement('div');
                strategyCard.className = 'card mb-3 strategy-card';
                strategyCard.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${strategy.name}</h5>
                        <p class="card-text">${strategy.description}</p>
                    </div>
                `;
                strategiesContainer.appendChild(strategyCard);
            });
        } else {
            strategiesContainer.innerHTML = '<p>No specific strategies found. Try providing more details about your experience.</p>';
        }

        // Show analysis if available
        if (data.analysis) {
            const analysisElement = document.getElementById('analysis-data');
            if (analysisElement) {
                let themesText = '';
                if (data.analysis.identified_themes) {
                    themesText = Object.keys(data.analysis.identified_themes).join(', ');
                }
                
                analysisElement.innerHTML = `
                    <p>We identified these themes in your sharing: <strong>${themesText || 'None'}</strong></p>
                `;
            }
        }

        // Show resources link
        document.getElementById('view-resources-btn').classList.remove('d-none');
    }

    /**
     * Update the UI based on the current state
     */
    updateUI(state, errorMessage = '') {
        const startBtn = document.getElementById('start-recording-btn');
        const stopBtn = document.getElementById('stop-recording-btn');
        const processBtn = document.getElementById('process-recording-btn');
        const recordingStatus = document.getElementById('recording-status');
        const recordingIndicator = document.getElementById('recording-indicator');

        switch (state) {
            case 'listening':
                startBtn.classList.add('d-none');
                stopBtn.classList.remove('d-none');
                processBtn.classList.add('d-none');
                recordingStatus.textContent = 'Listening...';
                recordingStatus.classList.remove('text-danger');
                recordingIndicator.classList.add('pulsating');
                break;
                
            case 'stopped':
                startBtn.classList.remove('d-none');
                stopBtn.classList.add('d-none');
                processBtn.classList.remove('d-none');
                recordingStatus.textContent = 'Recording stopped';
                recordingIndicator.classList.remove('pulsating');
                break;
                
            case 'processing':
                startBtn.classList.add('d-none');
                stopBtn.classList.add('d-none');
                processBtn.classList.add('d-none');
                recordingStatus.textContent = 'Processing your input...';
                document.getElementById('processing-spinner').classList.remove('d-none');
                break;
                
            case 'completed':
                startBtn.classList.remove('d-none');
                stopBtn.classList.add('d-none');
                processBtn.classList.add('d-none');
                recordingStatus.textContent = 'Ready to listen';
                document.getElementById('processing-spinner').classList.add('d-none');
                break;
                
            case 'error':
                startBtn.classList.remove('d-none');
                stopBtn.classList.add('d-none');
                processBtn.classList.add('d-none');
                recordingStatus.textContent = `Error: ${errorMessage}`;
                recordingStatus.classList.add('text-danger');
                recordingIndicator.classList.remove('pulsating');
                document.getElementById('processing-spinner').classList.add('d-none');
                break;
        }
    }

    /**
     * Show an error message to the user
     */
    showError(message) {
        const errorAlert = document.getElementById('error-alert');
        const errorMessage = document.getElementById('error-message');
        
        errorMessage.textContent = message;
        errorAlert.classList.remove('d-none');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorAlert.classList.add('d-none');
        }, 5000);
    }

    /**
     * Show browser support error
     */
    showBrowserSupportError() {
        const voiceContainer = document.getElementById('voice-container');
        voiceContainer.innerHTML = `
            <div class="alert alert-warning" role="alert">
                <h4 class="alert-heading">Browser Not Supported</h4>
                <p>Your browser doesn't support voice recognition. Please try using Google Chrome, Microsoft Edge, or Safari.</p>
            </div>
        `;
    }
}

// Create and export the voice interaction instance
const voiceInteraction = new VoiceInteraction();
