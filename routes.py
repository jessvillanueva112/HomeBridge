from flask import render_template, request, jsonify, session, redirect, url_for, flash
from app import app, db
from models import User, Entry, Strategy, Resource
from ml_processor import analyze_text, generate_strategies
import logging

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard page"""
    # In a real app, you'd check if user is logged in
    # For MVP, we'll proceed without authentication
    entries = Entry.query.order_by(Entry.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', entries=entries)

@app.route('/resources')
def resources():
    """Resources page"""
    campus_resources = Resource.query.filter_by(category='campus').all()
    online_resources = Resource.query.filter_by(category='online').all()
    community_resources = Resource.query.filter_by(category='community').all()
    
    return render_template('resources.html', 
                          campus_resources=campus_resources,
                          online_resources=online_resources,
                          community_resources=community_resources)

@app.route('/process_voice', methods=['POST'])
def process_voice():
    """Process voice input from the user"""
    try:
        text = request.json.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze the text for sentiment and key themes
        analysis_results = analyze_text(text)
        
        # Generate resilience strategies based on the analysis
        strategies = generate_strategies(analysis_results)
        
        # Store the entry in the database
        new_entry = Entry(
            content=text,
            sentiment_score=analysis_results.get('sentiment_score', 0),
            user_id=1  # For MVP, we'll use a default user ID
        )
        db.session.add(new_entry)
        db.session.flush()  # Get the new entry ID without committing
        
        # Store the strategies
        for strategy_data in strategies:
            new_strategy = Strategy(
                name=strategy_data['name'],
                description=strategy_data['description'],
                entry_id=new_entry.id
            )
            db.session.add(new_strategy)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'entry_id': new_entry.id,
            'strategies': strategies,
            'analysis': analysis_results
        })
    
    except Exception as e:
        logging.error(f"Error processing voice input: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/get_strategies/<int:entry_id>')
def get_strategies(entry_id):
    """Get strategies for a specific entry"""
    strategies = Strategy.query.filter_by(entry_id=entry_id).all()
    return jsonify({
        'strategies': [
            {
                'name': strategy.name,
                'description': strategy.description
            } for strategy in strategies
        ]
    })

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# Initialize the database with some sample resources
@app.before_first_request
def initialize_db():
    # Only add resources if none exist
    if Resource.query.count() == 0:
        resources = [
            Resource(
                title="UBC International Student Guide",
                description="Official guide for international students at UBC",
                category="campus",
                url="https://students.ubc.ca/international-student-guide"
            ),
            Resource(
                title="UBC Counseling Services",
                description="Mental health services available to UBC students",
                category="campus",
                url="https://students.ubc.ca/health/counselling-services"
            ),
            Resource(
                title="International Student Advising",
                description="Support for international students at UBC",
                category="campus",
                url="https://students.ubc.ca/about-student-services/international-student-advising"
            ),
            Resource(
                title="Headspace Meditation App",
                description="App for meditation and mindfulness",
                category="online",
                url="https://www.headspace.com/"
            ),
            Resource(
                title="7 Cups - Online Therapy",
                description="Free emotional support and online therapy",
                category="online",
                url="https://www.7cups.com/"
            ),
            Resource(
                title="International House UBC",
                description="Community for international students",
                category="community",
                url="https://global.ubc.ca/"
            ),
            Resource(
                title="Vancouver Multicultural Society",
                description="Local community support for newcomers",
                category="community",
                url="https://www.greatervancouver.org/"
            )
        ]
        
        for resource in resources:
            db.session.add(resource)
        
        db.session.commit()
