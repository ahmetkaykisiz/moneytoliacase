from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# SQLite veritabanı dosyası için klasör oluştur
if not os.path.exists("./data"):
    os.makedirs("./data")

# SQLite URL'si
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/urlshortener.db"

# SQLite için connect_args eklemeliyiz
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 