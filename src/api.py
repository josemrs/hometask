"""API request routing using FastAPI"""

import datetime
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import (
    User,
    PutDateOfBirth,
    GetUsernameResponse,
)  # pylint: disable=import-error
from db import get_db  # pylint: disable=import-error

api = FastAPI()


@api.put("/hello/{username}", status_code=204)
async def create_user(
    username: str, date_of_birth: PutDateOfBirth, db: Session = Depends(get_db)
) -> None:
    """Serving PUT /hello/<username> { “dateOfBirth”: “YYYY-MM-DD” } requests"""

    if not username.isalpha():
        raise HTTPException(
            status_code=400, detail="Username must contain only letters."
        )

    if date_of_birth.dateOfBirth >= datetime.date.today():
        raise HTTPException(
            status_code=400,
            detail="The date of birth must be a date before the today date",
        )

    db_user = User(username=username, date_of_birth=date_of_birth.dateOfBirth)

    try:
        db.merge(db_user)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=404, detail="Error inserting or updating user"
        ) from e

    return None


@api.get("/hello/{username}")
async def get_user(username: str, db: Session = Depends(get_db)) -> GetUsernameResponse:
    """Serving Get /hello/<username> requests { “date_of_birth”: “YYYY-MM-DD” } requests"""

    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    today = datetime.date.today()
    birthday_this_year = db_user.date_of_birth.replace(year=today.year)

    if birthday_this_year == today:
        return GetUsernameResponse(
            message=f"Hello, {db_user.username}! Happy birthday!"
        )

    days_remaining = birthday_this_year - today
    if days_remaining.days < 0:
        birthday_next_year = birthday_this_year.replace(year=today.year + 1)
        days_remaining = birthday_next_year - today

    return GetUsernameResponse(
        message=f"Hello, {db_user.username}! Your birthday is in {days_remaining.days} day(s)"
    )
