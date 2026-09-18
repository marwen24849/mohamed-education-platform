import os
os.chdir(r'C:\Users\marwe\Desktop\mohamed')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pathlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    print('root_path', app.root_path)
    print('engine_url', db.engine.url)
    print('cwd_exists', os.path.isdir('instance'))
    p = pathlib.Path('instance/database.db').resolve()
    print('resolved', p)
    print('exists', p.exists())
