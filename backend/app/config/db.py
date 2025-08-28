from sqlalchemy import create_engine
from app.config.settings import Settings
from sqlalchemy.orm import sessionmaker, Session

settings     = Settings()
engine       = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()