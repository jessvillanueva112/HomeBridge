from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Interaction, ProgressLog, Feedback, Resource
from .ml_processor import process_voice_input, load_resilience_strategies
import json
import datetime
import logging

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

# Simulated user for MVP without full authentication
DEMO_USER_ID = 1

@main.route('/')
def index():
    if not current_user.is_authenticated:
        demo_user = User.query.filter_by(username='demo').first()
        if not demo_user:
            demo_user = User(username='demo', email='demo@example.com')
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            db.session.commit()
        login_user(demo_user)
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        from models import User
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/process_voice', methods=['POST'])
@login_required
def process_voice():
    try:
        text = request.json.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
            
        response = process_voice_input(text)
        
        # Log the interaction
        interaction = Interaction(
            user_id=current_user.id,
            input_text=text,
            response_text=response
        )
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error processing voice input: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/resources')
@login_required
def resources():
    category = request.args.get('category', 'all')
    if category == 'all':
        resources = Resource.query.all()
    else:
        resources = Resource.query.filter_by(category=category).all()
    return render_template('resources.html', resources=resources)

@main.route('/log_progress', methods=['POST'])
def log_progress():
    from models import ProgressLog
    from app import db
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        log = ProgressLog(
            user_id=DEMO_USER_ID,
            mood_score=data.get('mood_score'),
            notes=data.get('notes')
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        logging.error(f"Error in log_progress: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        rating = request.form.get('rating')
        comments = request.form.get('comments')
        
        if rating:
            feedback = Feedback(
                user_id=current_user.id,
                rating=rating,
                comments=comments
            )
            db.session.add(feedback)
            db.session.commit()
            flash('Thank you for your feedback!', 'success')
            return redirect(url_for('main.index'))
            
    return render_template('feedback.html')

@main.route('/progress')
@login_required
def progress():
    logs = ProgressLog.query.filter_by(user_id=current_user.id).order_by(ProgressLog.created_at.desc()).all()
    return render_template('progress.html', logs=logs)
