from . import db


class DocumentType(db.Model):
    __tablename__ = 'document_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    documents = db.relationship('Document', backref='document_type', lazy=True)

    def __repr__(self):
        return f'<DocumentType {self.name}>'
