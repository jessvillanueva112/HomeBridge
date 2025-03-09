from flask import render_template, request, jsonify, redirect, url_for, flash, session
from app import app, db
from models import User, Interaction, ProgressLog, Feedback, Resource
from ml_processor import analyze_text, get_resilience_strategies
from werkzeug.security import generate_password_hash, check_password_hash
import json
import datetime
import logging

# Simulated user for MVP without full authentication
DEMO_USER_ID = 1

@app.route('/')
def index():
    # Check if demo user exists, create if not
    if not User.query.get(DEMO_USER_ID):
        demo_user = User(
            id=DEMO_USER_ID,
            username="demo_user",
            email="demo@example.com",
            password_hash=generate_password_hash("demo_password")
        )
        db.session.add(demo_user)
        db.session.commit()
        
    return render_template('index.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    try:
        # Get transcript from request
        data = request.json
        transcript = data.get('transcript', '')
        
        if not transcript:
            logging.warning("Empty transcript received in process_voice")
            return jsonify({'error': 'No transcript provided'}), 400
        
        logging.info(f"Processing voice transcript: {transcript[:50]}...")
        
        # Process the text with ML
        try:
            sentiment_score, homesickness_level = analyze_text(transcript)
            logging.info(f"Analysis results: sentiment={sentiment_score}, homesickness={homesickness_level}")
        except Exception as e:
            logging.error(f"Error in analyze_text: {str(e)}")
            # Use default values if analysis fails
            sentiment_score, homesickness_level = 0.0, 5
        
        # Get resilience strategies
        try:
            strategies = get_resilience_strategies(transcript, homesickness_level)
            logging.info(f"Retrieved {len(strategies)} strategies")
        except Exception as e:
            logging.error(f"Error in get_resilience_strategies: {str(e)}")
            # Create default strategies if retrieval fails
            strategies = [
                {
                    "title": "Connect with Others",
                    "description": "Spend time with friends or reach out to family back home.",
                    "steps": ["Call a family member", "Meet a friend for coffee", "Join a student club"]
                },
                {
                    "title": "Self-Care Practice",
                    "description": "Take time for activities that help you relax and recharge.",
                    "steps": ["Get adequate sleep", "Eat nutritious meals", "Take time for hobbies"]
                }
            ]
        
        # Save the interaction to database
        try:
            interaction = Interaction(
                user_id=DEMO_USER_ID,
                transcript=transcript,
                sentiment_score=sentiment_score,
                homesickness_level=homesickness_level,
                recommended_strategies=json.dumps(strategies)
            )
            db.session.add(interaction)
            db.session.commit()
            interaction_id = interaction.id
            logging.info(f"Saved interaction with ID: {interaction_id}")
        except Exception as e:
            logging.error(f"Error saving interaction to database: {str(e)}")
            interaction_id = None
        
        # Return response
        return jsonify({
            'success': True,
            'sentiment_score': sentiment_score,
            'homesickness_level': homesickness_level,
            'strategies': strategies,
            'interaction_id': interaction_id
        })
        
    except Exception as e:
        logging.error(f"Unhandled error in process_voice: {str(e)}")
        # Return a user-friendly error
        return jsonify({
            'success': False,
            'error': "Sorry, we encountered an issue processing your input. Please try again.",
            'sentiment_score': 0.0,
            'homesickness_level': 5,
            'strategies': [
                {
                    "title": "Try Again Later",
                    "description": "We're experiencing technical difficulties. Please try again in a few moments.",
                    "steps": ["Refresh the page", "Try speaking more clearly", "Use the text input option if voice isn't working"]
                }
            ]
        }), 500

@app.route('/resources')
def resources():
    # Get resources from database or predefined list
    resources = Resource.query.all()
    
    # If no resources in DB, use the static JSON file
    if not resources:
        with open('static/data/resources.json', 'r') as f:
            resource_data = json.load(f)
            
        # Create resource objects for display
        resources = []
        for item in resource_data:
            resources.append({
                'title': item['title'],
                'description': item['description'],
                'category': item['category'],
                'url': item.get('url', ''),
                'contact_info': item.get('contact_info', '')
            })
    
    return render_template('resources.html', resources=resources)

@app.route('/progress')
def progress():
    # Get user's progress logs
    logs = ProgressLog.query.filter_by(user_id=DEMO_USER_ID).order_by(ProgressLog.timestamp.desc()).all()
    interactions = Interaction.query.filter_by(user_id=DEMO_USER_ID).order_by(Interaction.timestamp.desc()).all()
    
    # Format data for charts
    dates = []
    mood_ratings = []
    homesickness_levels = []
    
    for log in logs:
        dates.append(log.timestamp.strftime('%Y-%m-%d'))
        mood_ratings.append(log.mood_rating)
    
    for interaction in interactions:
        if interaction.homesickness_level:
            dates.append(interaction.timestamp.strftime('%Y-%m-%d'))
            homesickness_levels.append(interaction.homesickness_level)
    
    return render_template('progress.html', 
                           logs=logs, 
                           interactions=interactions,
                           dates=json.dumps(dates),
                           mood_ratings=json.dumps(mood_ratings),
                           homesickness_levels=json.dumps(homesickness_levels))

@app.route('/add_progress_log', methods=['POST'])
def add_progress_log():
    try:
        mood_rating = int(request.form.get('mood_rating'))
        gratitude_entry = request.form.get('gratitude_entry', '')
        activities_completed = request.form.get('activities_completed', '')
        
        log = ProgressLog(
            user_id=DEMO_USER_ID,
            mood_rating=mood_rating,
            gratitude_entry=gratitude_entry,
            activities_completed=activities_completed
        )
        db.session.add(log)
        db.session.commit()
        
        flash('Progress logged successfully!', 'success')
        return redirect(url_for('progress'))
    except Exception as e:
        flash(f'Error logging progress: {str(e)}', 'danger')
        return redirect(url_for('progress'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        try:
            rating = int(request.form.get('rating'))
            comments = request.form.get('comments', '')
            
            feedback = Feedback(
                user_id=DEMO_USER_ID,
                rating=rating,
                comments=comments
            )
            db.session.add(feedback)
            db.session.commit()
            
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error submitting feedback: {str(e)}', 'danger')
    
    return render_template('feedback.html')
