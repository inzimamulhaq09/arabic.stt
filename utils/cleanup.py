import os
import time
from datetime import datetime, timedelta
from config import Config

def cleanup_old_files():
    """Clean up old recording and transcription files"""
    max_age = timedelta(days=Config.MAX_FILE_AGE_DAYS)
    now = datetime.now()
    
    # Clean recordings
    for filename in os.listdir(Config.UPLOAD_FOLDER):
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        if now - file_time > max_age:
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error removing file {filepath}: {e}")
                
    # Clean transcriptions
    for filename in os.listdir(Config.TRANSCRIPTION_FOLDER):
        filepath = os.path.join(Config.TRANSCRIPTION_FOLDER, filename)
        file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        if now - file_time > max_age:
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error removing file {filepath}: {e}")
