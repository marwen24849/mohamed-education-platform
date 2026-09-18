import os
from flask import Flask, render_template
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from config import BASE_DIR, DATABASE_URL, SECRET_KEY, UPLOAD_FOLDER, MAX_CONTENT_LENGTH

os.chdir(BASE_DIR)
os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Database
from models import db

db.init_app(app)

# Blueprints
from routes.public import public_bp
from routes.admin import admin_bp
from routes.auth import auth_bp

app.register_blueprint(public_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp)

# Ensure directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Import models after app/db creation
from models import Document, Subject, Level, DocumentType, Tag, AdminUser


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


def ensure_database_exists():
    try:
        url = make_url(DATABASE_URL)
    except Exception:
        return

    if url.get_backend_name() != 'mysql':
        return

    db_name = url.database
    if not db_name:
        return

    admin_url = url.set(database='mysql')
    engine = create_engine(admin_url)
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))


def init_seed_data():
    ensure_database_exists()
    from services.seed_service import seed_initial_data
    with app.app_context():
        db.create_all()
        seed_initial_data()


if __name__ == '__main__':
    init_seed_data()
    app.run(debug=True, host='127.0.0.1', port=5000)
