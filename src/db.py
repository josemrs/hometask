"""BD handling"""

from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE URL taken from environment variables or default for test
DATABASE_HOST = environ.get("DATABASE_HOST", "db")
DATABASE_USER = environ.get("DATABASE_USER", "test")
DATABASE_PASS = environ.get("DATABASE_PASS", "test")
DATABASE_PORT = environ.get("DATABASE_PORT", "5432")
DATABASE_NAME = environ.get("DATABASE_NAME", "hello")
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

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
