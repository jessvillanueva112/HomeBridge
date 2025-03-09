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

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set environment variables:
   - `DATABASE_URL` (optional, defaults to SQLite)
   - `SESSION_SECRET` (required for secure sessions)
   - `GEMINI_API_KEY` (required for Gemini AI integration)

## Running the Application

There are multiple ways to run the HomeBridge application:

### Option 1: Using Python Directly (Flask Interface)
```
python main.py
```
This runs the Flask application in development mode with debug features enabled.

### Option 2: Using Gunicorn (Recommended for Production)
```
gunicorn --bind 0.0.0.0:8080 --reuse-port --reload main:app
```
This starts the Flask server with automatic reloading when code changes are detected.

### Option 3: Using Streamlit (Interactive Dashboard)
```
streamlit run streamlit_app.py
```
This starts the Streamlit interactive dashboard, which provides enhanced visualization and analytics features.

### Option 4: One-line Installation and Run
```
pip install -r requirements.txt && gunicorn --bind 0.0.0.0:8080 --reuse-port --reload main:app
```
This installs all dependencies and starts the server in one command.

The Flask application will be available at http://0.0.0.0:8080 after starting with methods 1, 2, or 4.
The Streamlit dashboard will be available at http://0.0.0.0:8501 when using method 3.

## Gemini AI Integration

HomeBridge integrates Google's Gemini AI to provide enhanced natural language understanding and personalized support:

1. **Advanced Sentiment Analysis**: Gemini AI analyzes the emotional content of student interactions with greater accuracy
2. **Personalized Resilience Strategies**: Strategies are tailored to individual needs using Gemini's understanding of context
3. **Psychological Insights**: The system leverages research on neuroplasticity and emotional processing

To enable Gemini AI features, you must set the `GEMINI_API_KEY` environment variable. You can obtain a key from the [Google AI Studio](https://makersuite.google.com/).

## Research-Backed Approach

HomeBridge is built on scientific research:

- **Neuroplasticity Potential**: Gratitude journaling increases dorsolateral prefrontal activity by 29%, creating cognitive buffers against emotional overwhelm (BMC Psychology)
- **AI Efficacy**: NLP systems trained on grief-related narratives can detect high-risk linguistic markers months before clinical diagnosis (MDPI)
- **Addressing Loneliness**: Designed to counter the 42% increase in reported loneliness among bereaved individuals since 2020