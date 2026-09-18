from . import db


class Level(db.Model):
    __tablename__ = 'levels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    documents = db.relationship('Document', backref='level', lazy=True)

    def __repr__(self):
        return f'<Level {self.name}>'
