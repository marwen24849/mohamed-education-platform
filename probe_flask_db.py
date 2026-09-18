import os
os.chdir(r'C:\Users\marwe\Desktop\mohamed')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print('uri', app.config['SQLALCHEMY_DATABASE_URI'])
with app.app_context():
    db.create_all()
    print('create_ok')
