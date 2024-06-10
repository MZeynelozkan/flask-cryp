# auth.py

from flask import Blueprint, request, redirect, url_for, session, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # Kullanıcı kaydı işlemi
    # User registration process
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='sha256')

    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        flash('Kayıt başarılı! Giriş yapabilirsiniz.')
    except sqlite3.IntegrityError:
        flash('Kullanıcı adı zaten mevcut!')
    conn.close()

    return redirect(url_for('views.upload_form'))

@auth_bp.route('/login', methods=['POST'])
def login():
    # Kullanıcı girişi işlemi
    # User login process
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        session['logged_in'] = True
        session['user_id'] = user[0]
        session['username'] = username
        flash('Giriş başarılı!')
    else:
        flash('Yanlış kullanıcı adı veya şifre!')

    return redirect(url_for('views.upload_form'))

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Kullanıcı çıkışı işlemi
    # User logout process
    session.clear()
    flash('Çıkış yaptınız.')
    return redirect(url_for('views.upload_form'))
