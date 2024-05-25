import os
import json

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(BASE_DIR, '..', 'config.json')) as config_file:
        config_data = json.load(config_file)
    
    SECRET_KEY = config_data.get('SECRET_KEY', 'supersecretkey')
    SIROPE_URL = "redis://localhost:8080"
