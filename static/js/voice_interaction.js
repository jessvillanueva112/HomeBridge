document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const voiceBtn = document.getElementById('voice-btn');
    const stopBtn = document.getElementById('stop-btn');
    const restartBtn = document.getElementById('restart-btn');
    const initialPrompt = document.getElementById('initial-prompt');
    const recordingIndicator = document.getElementById('recording-indicator');
    const processingIndicator = document.getElementById('processing-indicator');
    const transcriptionResult = document.getElementById('transcription-result');
    const transcriptText = document.getElementById('transcript-text');
    const sentimentBar = document.getElementById('sentiment-bar');
    const sentimentDescription = document.getElementById('sentiment-description');
    const homesicknessBar = document.getElementById('homesickness-bar');
    const homesicknessDescription = document.getElementById('homesickness-description');
    const strategiesContainer = document.getElementById('strategies-container');
    const recordingTime = document.getElementById('recording-time');
    
    // Speech recognition
    let recognition;
    let recordingStartTime;
    let recordingTimer;
    let finalTranscript = '';
    
    // Check for browser speech API support and show appropriate UI
    checkBrowserSupport();
    
    function checkBrowserSupport() {
        if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
            console.warn("Speech recognition not supported in this browser");
            
            if (voiceBtn) {
                // Create a text input alternative
                createTextInputAlternative();
            }
        }
    }
    
    function createTextInputAlternative() {
        // Add a warning about browser compatibility
        const warningDiv = document.createElement('div');
        warningDiv.className = 'alert alert-warning mt-3';
        warningDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            Voice recognition is not supported in your browser. 
            You can type your thoughts below instead.
        `;
        
        // Create text input alternative
        const textInputForm = document.createElement('div');
        textInputForm.className = 'mt-4';
        textInputForm.innerHTML = `
            <div class="mb-3">
                <label for="text-input" class="form-label">Share how you're feeling about being far from home:</label>
                <textarea id="text-input" class="form-control" rows="4" 
                    placeholder="Type about your experience as an international student, what you miss about home, or challenges you're facing..."></textarea>
            </div>
            <div class="d-grid">
                <button id="submit-text-btn" class="btn btn-info">
                    <i class="fas fa-paper-plane me-2"></i>Submit
                </button>
            </div>
        `;
        
        // Add to the page
        const container = voiceBtn.closest('.d-flex');
        container.style.display = 'none';
        container.parentNode.appendChild(warningDiv);
        container.parentNode.appendChild(textInputForm);
        
        // Add event listener for the submit button
        document.getElementById('submit-text-btn').addEventListener('click', function() {
            const textInput = document.getElementById('text-input');
            const transcript = textInput.value.trim();
            
            if (transcript) {
                initialPrompt.style.display = 'none';
                processingIndicator.style.display = 'block';
                transcriptText.textContent = transcript;
                processTranscript(transcript);
            } else {
                alert('Please enter some text before submitting.');
            }
        });
    }
    
    // Initialize speech recognition
    function initSpeechRecognition() {
        // Check browser support
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            
            // Set properties
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            
            // Reset transcript when starting a new recording
            finalTranscript = '';
            
            // Handle results
            recognition.onresult = function(event) {
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript + ' ';
                    } else {
                        interimTranscript += transcript;
                    }
                }
                
                // Update transcript display
                transcriptText.innerHTML = 
                    finalTranscript + 
                    '<span class="text-muted">' + interimTranscript + '</span>';
                
                // Log for debugging
                console.log("Recognition captured:", finalTranscript);
            };
            
            // Handle errors
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                
                if (event.error === 'no-speech') {
                    alert('No speech was detected. Please try again and speak clearly into your microphone.');
                } else if (event.error === 'audio-capture') {
                    alert('No microphone was found or microphone is disabled. Please ensure your microphone is connected and enabled.');
                } else if (event.error === 'not-allowed') {
                    alert('Permission to use microphone was denied. Please allow microphone access to use this feature.');
                } else {
                    alert('There was an error with the speech recognition: ' + event.error);
                }
                
                stopRecording();
            };
            
            // Handle end of speech
            recognition.onend = function() {
                console.log("Speech recognition ended");
                // We don't call stopRecording here because we want to manually control when to stop
            };
            
            return true;
        } else {
            alert('Sorry, your browser does not support speech recognition. Try using Chrome or Edge, or use the text input option.');
            return false;
        }
    }
    
    // Start recording
    function startRecording() {
        if (!initSpeechRecognition()) return;
        
        // Show recording UI
        initialPrompt.style.display = 'none';
        recordingIndicator.style.display = 'block';
        
        // Clear previous transcripts
        transcriptText.innerHTML = '';
        finalTranscript = '';
        
        // Start recognition
        try {
            console.log("Starting speech recognition...");
            recognition.start();
            recordingStartTime = Date.now();
            
            // Start recording timer
            updateRecordingTime();
            recordingTimer = setInterval(updateRecordingTime, 1000);
        } catch (error) {
            console.error('Error starting speech recognition:', error);
            alert('Error starting speech recognition. Please refresh and try again.');
        }
    }
    
    // Stop recording
    function stopRecording() {
        console.log("Stopping recording...");
        
        // Stop recognition
        if (recognition) {
            try {
                recognition.stop();
                console.log("Recognition stopped");
            } catch (err) {
                console.error("Error stopping recognition:", err);
            }
        }
        
        // Stop recording timer
        clearInterval(recordingTimer);
        
        // Show processing UI
        recordingIndicator.style.display = 'none';
        processingIndicator.style.display = 'block';
        
        // Get transcript text
        const transcript = transcriptText.textContent.trim();
        console.log("Final transcript:", transcript);
        
        // Process the transcript
        if (transcript) {
            processTranscript(transcript);
        } else {
            // Fallback for demo mode or if no speech was detected
            const demoText = "I've been feeling really homesick lately. I miss my family and friends back home, and I'm struggling to connect with people here. It's hard to adjust to the new food and culture. Sometimes I feel very lonely and sad.";
            
            if (confirm('No speech was detected. Would you like to use a sample text to demonstrate the app?')) {
                transcriptText.textContent = demoText;
                processTranscript(demoText);
            } else {
                alert('Please try again and speak clearly into your microphone.');
                resetUI();
            }
        }
    }
    
    // Process transcript with the backend
    function processTranscript(transcript) {
        console.log("Processing transcript:", transcript);
        
        fetch('/process_voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ transcript: transcript })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log("Response from server:", data);
            
            // Show results UI
            processingIndicator.style.display = 'none';
            transcriptionResult.style.display = 'block';
            
            // Update sentiment display
            const sentimentScore = data.sentiment_score;
            const sentimentPercent = Math.round((sentimentScore + 1) * 50); // Convert -1 to 1 to 0-100%
            
            sentimentBar.style.width = sentimentPercent + '%';
            sentimentBar.textContent = sentimentPercent + '%';
            sentimentBar.setAttribute('aria-valuenow', sentimentPercent);
            
            // Set bar color based on sentiment
            if (sentimentScore < -0.3) {
                sentimentBar.className = 'progress-bar bg-danger';
                sentimentDescription.textContent = 'Your responses indicate feelings of sadness or distress. This is common when adjusting to a new environment.';
            } else if (sentimentScore < 0.3) {
                sentimentBar.className = 'progress-bar bg-warning';
                sentimentDescription.textContent = 'Your responses indicate mixed emotions. It's normal to have both positive and challenging experiences during adjustment.';
            } else {
                sentimentBar.className = 'progress-bar bg-success';
                sentimentDescription.textContent = 'Your responses indicate positive emotions. Maintaining this outlook will help with adjustment.';
            }
            
            // Update homesickness display
            const homesicknessLevel = data.homesickness_level;
            const homesicknessPercent = homesicknessLevel * 10;
            
            homesicknessBar.style.width = homesicknessPercent + '%';
            homesicknessBar.textContent = homesicknessLevel + '/10';
            homesicknessBar.setAttribute('aria-valuenow', homesicknessLevel);
            
            // Set homesickness description
            if (homesicknessLevel >= 7) {
                homesicknessDescription.textContent = 'Your responses suggest you may be experiencing significant homesickness. The strategies below are designed to help you address these feelings.';
            } else if (homesicknessLevel >= 4) {
                homesicknessDescription.textContent = 'Your responses suggest moderate homesickness. This is a common experience among international students.';
            } else {
                homesicknessDescription.textContent = 'Your responses suggest mild homesickness. The strategies below can help you maintain your emotional well-being.';
            }
            
            // Display strategies
            const strategies = data.strategies;
            strategiesContainer.innerHTML = '';
            
            strategies.forEach(strategy => {
                const strategyCard = document.createElement('div');
                strategyCard.className = 'col-md-4 mb-3';
                
                strategyCard.innerHTML = `
                    <div class="card h-100 shadow-sm strategy-card">
                        <div class="card-body">
                            <h5 class="card-title">${strategy.title}</h5>
                            <p class="card-text">${strategy.description}</p>
                            <h6>Steps:</h6>
                            <ul class="list-unstyled">
                                ${strategy.steps.map(step => `
                                    <li class="step-item">
                                        <i class="fas fa-chevron-right text-info"></i>
                                        <span>${step}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>
                `;
                
                strategiesContainer.appendChild(strategyCard);
            });
        })
        .catch(error => {
            console.error('Error processing transcript:', error);
            alert('There was an error processing your input. Please try again.');
            resetUI();
        });
    }
    
    // Update recording time display
    function updateRecordingTime() {
        const elapsedTime = Math.floor((Date.now() - recordingStartTime) / 1000);
        const minutes = Math.floor(elapsedTime / 60).toString().padStart(2, '0');
        const seconds = (elapsedTime % 60).toString().padStart(2, '0');
        recordingTime.textContent = `${minutes}:${seconds}`;
    }
    
    // Reset UI to initial state
    function resetUI() {
        transcriptText.textContent = '';
        finalTranscript = '';
        initialPrompt.style.display = 'block';
        recordingIndicator.style.display = 'none';
        processingIndicator.style.display = 'none';
        transcriptionResult.style.display = 'none';
        strategiesContainer.innerHTML = '';
    }
    
    // Event listeners
    if (voiceBtn) voiceBtn.addEventListener('click', startRecording);
    if (stopBtn) stopBtn.addEventListener('click', stopRecording);
    if (restartBtn) restartBtn.addEventListener('click', resetUI);
});
