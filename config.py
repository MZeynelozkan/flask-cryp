import os

class Config:
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 1024 * 1024 * 16  # 16 MB limit
    DATABASE = 'files.db'
