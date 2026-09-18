import config
from sqlalchemy import create_engine, text

print(config.DATABASE_URL)
engine = create_engine(config.DATABASE_URL)
try:
    conn = engine.connect()
    print(conn.execute(text('SELECT 1')).fetchall())
    conn.close()
except Exception as e:
    print(type(e).__name__, e)
