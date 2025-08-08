import os

class Config:
    # Base configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recordings')
    TRANSCRIPTION_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'transcriptions')
    ALLOWED_EXTENSIONS = {'wav'}
    MAX_FILE_AGE_DAYS = 30  # Auto-cleanup files older than this

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Add production-specific settings
    DATABASE_URI = os.environ.get('DATABASE_URI')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    # Add development-specific settings

# Select configuration based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
