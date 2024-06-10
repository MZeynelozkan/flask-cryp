import os
import io
import base64
import sqlite3
from flask import Flask, request, redirect, url_for, send_file, render_template, flash
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.urandom(24)  # Use a stronger random key
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 16 # 16 MB limit 
#... (rest of the code is the same as the original code)


def init_db():
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            key TEXT,
            salt BLOB
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def generate_key(password: str, salt: bytes):
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = f.encrypt(original)
    with open(file_path, 'wb') as file:
        file.write(encrypted)

def decrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    with open(file_path, 'wb') as file:
        file.write(decrypted)

@app.route('/')
def upload_form():
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute("SELECT id, filename FROM files")
    files = c.fetchall()
    conn.close()
    files_list = [{'id': file[0], 'filename': file[1]} for file in files]

    return render_template('index.html', files=files_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    password = request.form['password']

    if file and password:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        salt = os.urandom(16)
        key = generate_key(password, salt)
        encrypt_file(file_path, key)

        conn = sqlite3.connect('files.db')
        c = conn.cursor()
        c.execute("INSERT INTO files (filename, key, salt) VALUES (?, ?, ?)", (filename, key.decode(), salt))
        conn.commit()
        conn.close()

        return redirect(url_for('upload_form'))
    else:
        return 'Dosya veya şifre eksik!', 400
@app.route('/download', methods=['POST'])
def download_file():
    file_id = request.form['file_id']
    password = request.form['password']

    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute("SELECT filename, key, salt FROM files WHERE id = ?", (file_id,))
    row = c.fetchone()
    conn.close()

    if row:
        filename = row[0]
        stored_key = row[1].encode()
        salt = row[2]
        key = generate_key(password, salt)

        if key == stored_key:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            temp_file_path = file_path + '.dec'

            decrypt_file(file_path, key)
            with open(file_path, 'rb') as f:
                data = f.read()

            # Re-encrypt the file
            encrypt_file(file_path, key)

            # Write the decrypted data to a temporary file for sending
            with open(temp_file_path, 'wb') as f:
                f.write(data)

            response = send_file(temp_file_path, as_attachment=True, download_name=filename)

            @response.call_on_close
            def cleanup():
                os.remove(temp_file_path)

            return response
        else:
            return 'Yanlış şifre!', 400
    else:
        return 'Dosya bulunamadı!', 404



@app.route('/delete', methods=['POST'])
def delete_file():
    file_id = request.form['file_id']
    password = request.form['password']

    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute("SELECT filename, key, salt FROM files WHERE id = ?", (file_id,))
    row = c.fetchone()
    conn.close()

    if row:
        filename = row[0]
        stored_key = row[1].encode()
        salt = row[2]
        key = generate_key(password, salt)

        if key == stored_key:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.remove(file_path)

            conn = sqlite3.connect('files.db')
            c = conn.cursor()
            c.execute("DELETE FROM files WHERE id = ?", (file_id,))
            conn.commit()
            conn.close()

            return redirect(url_for('upload_form'))
        else:
            return 'Yanlış şifre!', 400
    else:
        return 'Dosya bulunamadı!', 404

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
