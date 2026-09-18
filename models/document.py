from datetime import datetime

from . import db


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, default=0)
    school_year = db.Column(db.String(50), nullable=True)
    author = db.Column(db.String(150), nullable=True)
    is_visible = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    allow_download = db.Column(db.Boolean, default=True)
    is_pinned = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    downloads = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=True)
    document_type_id = db.Column(db.Integer, db.ForeignKey('document_types.id'), nullable=True)

    def __repr__(self):
        return f'<Document {self.title}>'
