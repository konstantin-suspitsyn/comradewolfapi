from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Connection for async and fastApi.Depends
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session():
    """
    To use before fast api start
    :return:
    """
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
