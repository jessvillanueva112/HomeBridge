from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    country_of_origin = db.Column(db.String(50))
    language_preference = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    profile = db.relationship('UserProfile', backref='user', uselist=False)
    mood_entries = db.relationship('MoodEntry', backref='user')
    gratitude_entries = db.relationship('GratitudeEntry', backref='user')
    strategies = db.relationship('UserStrategies', backref='user')
    resources = db.relationship('UserResources', backref='user')
    voice_interactions = db.relationship('VoiceInteractions', backref='user')
    groups = db.relationship('UserGroups', backref='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    preferred_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    program = db.Column(db.String(100))
    year_of_study = db.Column(db.Integer)
    arrival_date = db.Column(db.Date)

class MoodEntry(db.Model):
    __tablename__ = 'mood_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood_score = db.Column(db.Integer, nullable=False)
    sentiment_score = db.Column(db.Float)
    homesickness_level = db.Column(db.Integer, nullable=False)
    entry_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GratitudeEntry(db.Model):
    __tablename__ = 'gratitude_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    entry_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ResilienceStrategy(db.Model):
    __tablename__ = 'resilience_strategies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    steps = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_strategies = db.relationship('UserStrategies', backref='resilience_strategy')

class UserStrategies(db.Model):
    __tablename__ = 'user_strategies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    strategy_id = db.Column(db.Integer, db.ForeignKey('resilience_strategies.id'), nullable=False)
    status = db.Column(db.String(20), default='suggested')
    tried_at = db.Column(db.DateTime)
    effectiveness_score = db.Column(db.Integer)
    notes = db.Column(db.Text)

class Resource(db.Model):
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200))
    contact_info = db.Column(db.Text)
    hours = db.Column(db.Text)
    url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_resources = db.relationship('UserResources', backref='resource')

class UserResources(db.Model):
    __tablename__ = 'user_resources'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    accessed_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer)
    feedback = db.Column(db.Text)

class VoiceInteractions(db.Model):
    __tablename__ = 'voice_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    audio_file_path = db.Column(db.String(255))
    transcript = db.Column(db.Text)
    sentiment_score = db.Column(db.Float)
    homesickness_level = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SupportGroup(db.Model):
    __tablename__ = 'support_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    meeting_time = db.Column(db.String(100))
    location = db.Column(db.String(200))
    contact_person = db.Column(db.String(100))
    contact_email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_groups = db.relationship('UserGroups', backref='support_group')

class UserGroups(db.Model):
    __tablename__ = 'user_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('support_groups.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), default='member')
