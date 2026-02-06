import os
import json

class Config:
    # Get parent directory (where main.py is located)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Data files in app root
    DATA_FILE = os.path.join(BASE_DIR, "pythorng_data.json")
    BACKUP_FILE = os.path.join(BASE_DIR, "pythorng_backup.json")
    
    # Security: Use environment variable for webhook. Never hardcode sensitive URLs
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    @staticmethod
    def get_launcher_data_file():
        return os.path.join(Config.DATA_FILE)
    
    @staticmethod
    def ensure_directories():
        os.makedirs(Config.BASE_DIR, exist_ok=True)
