import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # UBC API Configuration
    UBC_API_KEY = os.getenv('UBC_API_KEY')
    UBC_API_BASE_URL = 'https://students.ubc.ca/api'
    
    # Qualtrics Configuration
    QUALTRICS_API_TOKEN = os.getenv('QUALTRICS_API_TOKEN')
    QUALTRICS_DATA_CENTER = os.getenv('QUALTRICS_DATA_CENTER', 'ca1')
    QUALTRICS_USER_SURVEY_ID = os.getenv('QUALTRICS_USER_SURVEY_ID')
    
    # OutSystems Configuration
    OUTSYSTEMS_API_KEY = os.getenv('OUTSYSTEMS_API_KEY')
    OUTSYSTEMS_TENANT = os.getenv('OUTSYSTEMS_TENANT')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///homebridge.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security Configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # External Service URLs
    UBC_COUNSELLING_URL = 'https://students.ubc.ca/health/counselling-services'
    UBC_STUDENT_SERVICES_URL = 'https://students.ubc.ca/about-student-services'
    UBC_EVENTS_URL = 'https://events.ubc.ca'
    
    # Sync Configuration
    SYNC_INTERVAL_HOURS = 1  # How often to sync data
    MAX_SYNC_ATTEMPTS = 3  # Maximum number of sync attempts before giving up
    
    # Sentiment Analysis Configuration
    SENTIMENT_CHANGE_THRESHOLD = 0.5  # Threshold for significant sentiment changes
    DEFAULT_SENTIMENT_HISTORY_DAYS = 30  # Default number of days to analyze
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Cache Configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = '200 per day'
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Feature Flags
    ENABLE_QUALTRICS = os.getenv('ENABLE_QUALTRICS', 'true').lower() == 'true'
    ENABLE_OUTSYSTEMS = os.getenv('ENABLE_OUTSYSTEMS', 'true').lower() == 'true'
    ENABLE_UBC_SYNC = os.getenv('ENABLE_UBC_SYNC', 'true').lower() == 'true'
    
    # Monitoring Configuration
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
    METRICS_PORT = int(os.getenv('METRICS_PORT', '9090'))
    
    # Backup Configuration
    BACKUP_DIR = os.getenv('BACKUP_DIR', 'backups')
    BACKUP_INTERVAL = int(os.getenv('BACKUP_INTERVAL', '86400'))  # Default: 24 hours
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration values are present"""
        required_vars = [
            'UBC_API_KEY',
            'SECRET_KEY',
            'DATABASE_URL',
            'QUALTRICS_API_TOKEN',
            'QUALTRICS_USER_SURVEY_ID'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise ValueError(f"Missing required configuration variables: {', '.join(missing_vars)}")
        
        return True 