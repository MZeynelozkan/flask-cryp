# config.py

import os

class Config:
    # Uygulama yapılandırma ayarları
    # Application configuration settings
    UPLOAD_FOLDER = 'uploads'
    SECRET_KEY = os.urandom(24)
    MAX_CONTENT_LENGTH = 1024 * 1024 * 16  # 16 MB limit
