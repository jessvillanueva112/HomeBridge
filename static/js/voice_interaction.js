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
            
            // Handle results
            let finalTranscript = '';
            
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
            };
            
            // Handle errors
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                stopRecording();
                alert('There was an error with the speech recognition: ' + event.error);
            };
            
            // Handle end of speech
            recognition.onend = function() {
                // This will fire when recognition stops
                // We don't call stopRecording here because we want to manually control when to stop
            };
            
            return true;
        } else {
            alert('Sorry, your browser does not support speech recognition. Try using Chrome or Edge.');
            return false;
        }
    }
    
    // Start recording
    function startRecording() {
        if (!initSpeechRecognition()) return;
        
        // Show recording UI
        initialPrompt.style.display = 'none';
        recordingIndicator.style.display = 'block';
        
        // Start recognition
        try {
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
        // Stop recognition
        if (recognition) {
            recognition.stop();
        }
        
        // Stop recording timer
        clearInterval(recordingTimer);
        
        // Show processing UI
        recordingIndicator.style.display = 'none';
        processingIndicator.style.display = 'block';
        
        // Get transcript text
        const transcript = transcriptText.textContent.trim();
        
        // Process the transcript
        if (transcript) {
            processTranscript(transcript);
        } else {
            alert('No speech detected. Please try again.');
            resetUI();
        }
    }
    
    // Process transcript with the backend
    function processTranscript(transcript) {
        fetch('/process_voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ transcript: transcript })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
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
            alert('There was an error processing your speech. Please try again.');
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
        initialPrompt.style.display = 'block';
        recordingIndicator.style.display = 'none';
        processingIndicator.style.display = 'none';
        transcriptionResult.style.display = 'none';
        strategiesContainer.innerHTML = '';
    }
    
    // Event listeners
    voiceBtn.addEventListener('click', startRecording);
    stopBtn.addEventListener('click', stopRecording);
    restartBtn.addEventListener('click', resetUI);
});
