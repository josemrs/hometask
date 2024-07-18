"""Pydantic and SqlAlchemy models"""

import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Date
from pydantic import BaseModel

Base = declarative_base()


class User(Base):
    """DB Model for user"""

    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    date_of_birth = Column("dateofbirth", Date, nullable=False, quote=False)


class PutDateOfBirth(BaseModel):
    """Pydantic model for PUT user request"""

    dateOfBirth: datetime.date


class GetUsernameResponse(BaseModel):
    """Pydanty model for Get username request"""

    message: str
