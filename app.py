import os
import logging
from dotenv import load_dotenv
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Load environment variables from .env file if it exists
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        app.config.from_envvar('APP_SETTINGS', silent=True)
        
        # Set default configuration
        app.config.setdefault('SQLALCHEMY_DATABASE_URI', 
            os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(app.instance_path, "homesickness.db")}'))
        app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        app.config.setdefault('SECRET_KEY', os.getenv('SESSION_SECRET', 'dev'))
    else:
        # Load the test config if passed in
        app.config.update(test_config)
        # Ensure test database uses a separate path
        if 'SQLALCHEMY_DATABASE_URI' not in test_config:
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "test.db")}'
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Initialize database
    with app.app_context():
        init_db()
    
    return app

def init_db():
    """Initialize the database with required tables."""
    try:
        # Import models here to avoid circular imports
        from models import User, Interaction, ProgressLog, Feedback, Resource
        
        # Create all tables
        db.create_all()
        
        # Create demo user if it doesn't exist
        if not User.query.filter_by(username='demo').first():
            demo_user = User(
                username='demo',
                email='demo@example.com',
                password_hash='demo_password_hash'  # This is just for testing
            )
            db.session.add(demo_user)
            db.session.commit()
            
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing database: {str(e)}")
        raise

# Only create the application instance if running this file directly
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5003)
