from . import db

document_tags = db.Table(
    'document_tags',
    db.Column('document_id', db.Integer, db.ForeignKey('documents.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    documents = db.relationship('Document', secondary=document_tags, backref='tags', lazy='dynamic')

    def __repr__(self):
        return f'<Tag {self.name}>'
