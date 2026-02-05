import os
import json

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    DATA_FILE = os.path.join(BASE_DIR, "pythorng_data.json")
    BACKUP_FILE = os.path.join(BASE_DIR, "pythorng_backup.json")
    
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://discordapp.com/api/webhooks/1394363482492899328/_WwfcDUrEMyorTU6euSq8FOI06ITyEJ_oJYFZxTNy1wPg8NnnwS3tHHnVyYQHfyhbY1q")
    
    @staticmethod
    def get_launcher_data_file():
        return os.path.join(Config.BASE_DIR, "pythorng_data.json")
    
    @staticmethod
    def ensure_directories():
        os.makedirs(Config.BASE_DIR, exist_ok=True)
