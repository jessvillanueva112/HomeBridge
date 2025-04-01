# HomeBridge: UBC International Student Support

HomeBridge is a voice-interactive web application designed to help international students at the University of British Columbia (UBC) cope with homesickness and adapt to their new environment.

## Overview

HomeBridge uses natural language processing, machine learning, and Google's Gemini AI to analyze students' spoken or written input about their experiences, then provides personalized resilience strategies and resources tailored to their needs.

## Features

- **Voice Interaction**: Speak naturally about your feelings and experiences to receive support
- **Advanced Sentiment Analysis**: AI-powered analysis of your emotional state and homesickness level using Gemini API
- **Personalized Strategies**: Receive tailored resilience strategies based on your specific situation
- **Progress Tracking**: Monitor your emotional well-being over time with mood tracking and visualization
- **Resource Directory**: Access UBC-specific resources for international students
- **Gratitude Practice**: Record things you're grateful for to improve well-being
- **Neuroplasticity Support**: Features designed based on research showing gratitude journaling increases dorsolateral prefrontal activity by 29%, creating cognitive buffers
- **Interactive Streamlit Dashboard**: Beautiful data visualizations and interactive interface

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Dashboard**: Streamlit for interactive data visualization
- **Database**: SQLite (with SQLAlchemy ORM)
- **NLP/ML**: NLTK, scikit-learn, Google Gemini AI
- **Data Visualization**: Plotly, Matplotlib, Seaborn

## Prerequisites

Before running HomeBridge, ensure you have:
1. Python 3.8 or higher installed
2. A Google Cloud account for the Gemini API key
3. Git installed (for cloning the repository)

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/HomeBridge.git
   cd HomeBridge
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   # You'll need to:
   # 1. Generate a secure SESSION_SECRET (you can use: python -c "import secrets; print(secrets.token_hex(32))")
   # 2. Get a GEMINI_API_KEY from Google AI Studio (https://makersuite.google.com/)
   # 3. Update other variables as needed
   ```

5. Install NLTK resources:
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```

## Running the Application

There are multiple ways to run HomeBridge:

### Option 1: Using Flask (Recommended for Development)
```bash
FLASK_APP=app.py flask run --port=5003
```
The application will be available at http://127.0.0.1:5003

Note: If port 5003 is in use, you can try other ports (e.g., 5004, 5005).

### Option 2: Using Python Directly
```bash
python main.py
```

### Option 3: Using Gunicorn (Recommended for Production)
```bash
gunicorn --bind 0.0.0.0:5003 --workers 4 app:app
```

### Option 4: Using Streamlit (Interactive Dashboard)
```bash
streamlit run streamlit_app.py
```
The Streamlit dashboard will be available at http://localhost:8501

## Troubleshooting

1. **Port Already in Use**: If you see "Address already in use", try:
   - Using a different port (e.g., 5003, 5004, 5005)
   - On macOS, check System Settings > General > AirDrop & Handoff for AirPlay settings

2. **NLTK Resources**: If you see NLTK-related errors:
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```

3. **Missing Dependencies**: If you encounter ModuleNotFoundError:
   ```bash
   pip install -r requirements.txt
   ```

## Gemini AI Integration

HomeBridge uses Google's Gemini AI for enhanced natural language understanding. To enable this:

1. Visit [Google AI Studio](https://makersuite.google.com/)
2. Create or select a project
3. Generate an API key
4. Add the key to your `.env` file:
   ```
   GEMINI_API_KEY=your_key_here
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Research-Backed Approach

HomeBridge is built on scientific research:
- **Neuroplasticity Potential**: Gratitude journaling increases dorsolateral prefrontal activity by 29%
- **AI Efficacy**: NLP systems trained on grief-related narratives can detect high-risk linguistic markers
- **Addressing Loneliness**: Designed to counter the 42% increase in reported loneliness among bereaved individuals