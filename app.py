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
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", os.urandom(24))

# configure the database, relative to the app instance folder
database_url = os.environ.get("DATABASE_URL", "sqlite:///homesickness.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20
}

# Add error handling for database connection
def init_db():
    try:
        with app.app_context():
            # Import models here to ensure they're registered
            from models import User, JournalEntry, MoodEntry, GratitudeEntry
            # Create all tables
            db.create_all()
            logging.info("Database initialized successfully")
            
            # Create demo user if it doesn't exist
            from routes import DEMO_USER_ID
            if not User.query.get(DEMO_USER_ID):
                demo_user = User(
                    id=DEMO_USER_ID,
                    username="demo_user",
                    email="demo@example.com",
                    password_hash="demo_password_hash"  # This is just for demo purposes
                )
                db.session.add(demo_user)
                db.session.commit()
                logging.info("Demo user created successfully")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        raise

# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

# Initialize database
init_db()

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

# Import routes after app and db are initialized
from routes import *

# Add health check endpoint for Render
@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200
