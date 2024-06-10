import os
import sqlite3
from flask import Blueprint, request, redirect, url_for, send_file, render_template, session, flash
from werkzeug.utils import secure_filename
from encryption import generate_key, encrypt_file, decrypt_file
from config import Config

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def upload_form():
    if 'logged_in' not in session:
        return render_template('index.html', files=[])

    user_id = session['user_id']

    conn = sqlite3.connect(Config.DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, filename FROM files WHERE user_id = ?", (user_id,))
    files = c.fetchall()
    conn.close()
    files_list = [{'id': file[0], 'filename': file[1]} for file in files]

    return render_template('index.html', files=files_list)

@views_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'logged_in' not in session:
        return 'Önce giriş yapmalısınız!', 401

    file = request.files['file']
    password = request.form['password']
    user_id = session['user_id']

    if file and password:
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)

        salt = os.urandom(16)
        key = generate_key(password, salt)
        encrypt_file(file_path, key)

        conn = sqlite3.connect(Config.DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO files (filename, key, salt, user_id) VALUES (?, ?, ?, ?)", (filename, key.decode(), salt, user_id))
        conn.commit()
        conn.close()

        return redirect(url_for('views.upload_form'))
    else:
        return 'Dosya veya şifre eksik!', 400

@views_bp.route('/download', methods=['POST'])
def download_file():
    if 'logged_in' not in session:
        return 'Önce giriş yapmalısınız!', 401

    file_id = request.form['file_id']
    password = request.form['password']
    user_id = session['user_id']

    conn = sqlite3.connect(Config.DATABASE)
    c = conn.cursor()
    c.execute("SELECT filename, key, salt FROM files WHERE id = ? AND user_id = ?", (file_id, user_id))
    row = c.fetchone()
    conn.close()

    if row:
        filename = row[0]
        stored_key = row[1].encode()
        salt = row[2]
        key = generate_key(password, salt)

        if key == stored_key:
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            temp_file_path = file_path + '.dec'

            decrypt_file(file_path, key)
            with open(file_path, 'rb') as f:
                data = f.read()

            encrypt_file(file_path, key)

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

@views_bp.route('/delete', methods=['POST'])
def delete_file():
    if 'logged_in' not in session:
        return 'Önce giriş yapmalısınız!', 401

    file_id = request.form['file_id']
    user_id = session['user_id']

    conn = sqlite3.connect(Config.DATABASE)
    c = conn.cursor()
    c.execute("SELECT filename FROM files WHERE id = ? AND user_id = ?", (file_id, user_id))
    row = c.fetchone()

    if row:
        filename = row[0]
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        c.execute("DELETE FROM files WHERE id = ?", (file_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('views.upload_form'))
    else:
        conn.close()
        return 'Dosya bulunamadı!', 404
