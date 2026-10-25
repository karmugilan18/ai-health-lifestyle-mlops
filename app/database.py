import os
from sqlalchemy import create_engine, text
URL = os.getenv("DATABASE_URL", "sqlite:///./assessments.db")
_engine = None
def engine():
    global _engine
    if _engine is None:
        _engine = create_engine(URL, pool_pre_ping=True, connect_args={"check_same_thread":False} if URL.startswith("sqlite") else {})
    return _engine
def init_db():
    try:
        with engine().begin() as c:
            if URL.startswith("sqlite"):
                c.execute(text("CREATE TABLE IF NOT EXISTS assessments (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, input_json TEXT NOT NULL, score FLOAT NOT NULL, risk_category TEXT NOT NULL)"))
            else:
                c.execute(text("CREATE TABLE IF NOT EXISTS assessments (id SERIAL PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, input_json TEXT NOT NULL, score FLOAT NOT NULL, risk_category VARCHAR(20) NOT NULL)"))
    except Exception as e: print("DB init warning:", e)
def save_assessment(input_json, score, risk):
    try:
        with engine().begin() as c:
            r = c.execute(text("INSERT INTO assessments (input_json,score,risk_category) VALUES (:i,:s,:r)"), {"i":input_json,"s":score,"r":risk})
            return r.lastrowid
    except Exception as e:
        print("DB save warning:", e); return None
def recent_assessments(limit=20):
    try:
        with engine().connect() as c:
            rows = c.execute(text("SELECT id, created_at, score, risk_category FROM assessments ORDER BY id DESC LIMIT :n"), {"n":limit}).fetchall()
        return [{"id":r[0],"created_at":str(r[1]),"score":float(r[2]),"risk_category":r[3]} for r in rows]
    except Exception as e:
        print("DB history warning:",e); return []
