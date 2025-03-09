from datetime import datetime
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    interactions = db.relationship('Interaction', backref='user', lazy=True)
    progress_logs = db.relationship('ProgressLog', backref='user', lazy=True)
    feedback = db.relationship('Feedback', backref='user', lazy=True)

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transcript = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.Float)
    homesickness_level = db.Column(db.Integer)  # Scale 1-10
    recommended_strategies = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ProgressLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood_rating = db.Column(db.Integer)  # Scale 1-10
    gratitude_entry = db.Column(db.Text)
    activities_completed = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer)  # Scale 1-5
    comments = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    url = db.Column(db.String(256))
    contact_info = db.Column(db.String(256))
