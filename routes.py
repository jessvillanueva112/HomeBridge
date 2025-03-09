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
        data = request.json
        transcript = data.get('transcript', '')
        
        if not transcript:
            return jsonify({'error': 'No transcript provided'}), 400
        
        # Process the text with ML
        sentiment_score, homesickness_level = analyze_text(transcript)
        strategies = get_resilience_strategies(transcript, homesickness_level)
        
        # Save the interaction
        interaction = Interaction(
            user_id=DEMO_USER_ID,
            transcript=transcript,
            sentiment_score=sentiment_score,
            homesickness_level=homesickness_level,
            recommended_strategies=json.dumps(strategies)
        )
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'sentiment_score': sentiment_score,
            'homesickness_level': homesickness_level,
            'strategies': strategies,
            'interaction_id': interaction.id
        })
    except Exception as e:
        logging.error(f"Error processing voice: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
