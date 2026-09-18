from . import db


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), default='📚')
    color = db.Column(db.String(20), default='#3b82f6')
    documents = db.relationship('Document', backref='subject', lazy=True)

    def __repr__(self):
        return f'<Subject {self.name}>'
