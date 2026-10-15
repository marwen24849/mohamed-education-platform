import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = Path(BASE_DIR) / 'instance'
UPLOAD_FOLDER = Path(BASE_DIR) / 'uploads'

INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

MYSQL_HOST = os.getenv('MYSQL_HOST', 'db')
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root_password')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'mohamed')

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'
)
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 15 * 1024 * 1024))

ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'zip', 'rar'
}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/plain',
    'application/zip',
    'application/x-rar-compressed',
    'application/x-zip-compressed',
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
