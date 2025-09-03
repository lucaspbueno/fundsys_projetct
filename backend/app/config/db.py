from sqlalchemy import create_engine
from .settings import get_settings
from sqlalchemy.orm import sessionmaker, Session

engine       = create_engine(get_settings().database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()