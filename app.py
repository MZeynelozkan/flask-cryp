import os
from flask import Flask
from config import Config
from database import init_db, add_user_id_column
from views import views_bp
from auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

init_db()
add_user_id_column()

app.register_blueprint(views_bp)
app.register_blueprint(auth_bp)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if __name__ == "__main__":
    app.run(debug=True)
