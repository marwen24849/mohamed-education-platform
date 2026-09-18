from sqlalchemy import create_engine
import os

base = os.path.abspath('instance/database.db')
paths = [
    base,
    base.replace('\\', '/'),
    'C:/Users/marwe/Desktop/mohamed/instance/database.db',
    'C:\\Users\\marwe\\Desktop\\mohamed\\instance\\database.db',
]
urls = [
    'sqlite:///' + base,
    'sqlite:///' + base.replace('\\', '/'),
    'sqlite:///C:/Users/marwe/Desktop/mohamed/instance/database.db',
    'sqlite:///C:\\Users\\marwe\\Desktop\\mohamed\\instance\\database.db',
    'sqlite:////' + base.replace('\\', '/'),
    'sqlite:////' + base,
]
print('base', base)
for url in urls:
    print('TRY', url)
    try:
        eng = create_engine(url)
        conn = eng.connect()
        conn.execute('SELECT 1')
        print('OK')
        conn.close()
    except Exception as e:
        print('ERR', type(e).__name__, e)
