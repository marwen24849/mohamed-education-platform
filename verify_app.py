from app import app
from models import db
from services.seed_service import seed_initial_data

with app.app_context():
    db.create_all()
    seed_initial_data()
    client = app.test_client()
    print('index', client.get('/').status_code)
    print('documents', client.get('/documents').status_code)
    print('login', client.get('/admin/login').status_code)
    resp = client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    print('login_post', resp.status_code, resp.headers.get('Location'))
    print('dashboard', client.get('/admin/').status_code)
    print('search', client.get('/search?q=math').status_code)
