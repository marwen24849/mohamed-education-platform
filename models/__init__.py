from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .admin_user import AdminUser
from .subject import Subject
from .level import Level
from .document_type import DocumentType
from .tag import Tag
from .document import Document
from .site_settings import SiteSettings
