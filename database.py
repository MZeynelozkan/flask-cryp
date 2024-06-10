# db.py

import sqlite3

def init_db():
    # Veritabanını başlatır ve gerekli tabloları oluşturur
    # Initializes the database and creates necessary tables
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    # Kullanıcılar tablosunun var olduğundan emin olur
    # Ensure the users table exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    # Dosyalar tablosunun var olduğundan ve user_id sütununu içerdiğinden emin olur
    # Ensure the files table exists and includes the user_id column
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            key TEXT,
            salt BLOB,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user_id_column():
    # Dosyalar tablosuna user_id sütunu ekler
    # Adds the user_id column to the files table
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute("PRAGMA table_info(files)")
    columns = [col[1] for col in c.fetchall()]
    if 'user_id' not in columns:
        c.execute("ALTER TABLE files ADD COLUMN user_id INTEGER")
        conn.commit()
    conn.close()

# Veritabanını başlat ve gerekli sütunu ekle
# Initialize the database and add the necessary column
init_db()
add_user_id_column()
