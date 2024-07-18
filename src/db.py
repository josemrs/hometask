"""BD handling"""

from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE URL taken from environment variables or default for test
DATABASE_URL = environ.get("DATABASE_URL", "postgresql://test:test@db:5432/hello")

# Connect to the DB and get a session maker
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get a Session with the DB"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
