"""Unit tests for Hello API"""
from unittest.mock import MagicMock
import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from models import User
from api import api, get_db

@pytest.fixture(scope="function")
def db_session():
    session = MagicMock()
    yield session

@pytest.fixture(scope='function')
def client(db_session):
    def override_get_db():
        yield db_session
    api.dependency_overrides[get_db] = override_get_db
    with TestClient(api) as c:
        yield c
    api.dependency_overrides.clear()

def test_create_user_valid_input(db_session, client):
    username = "testuser"
    date_of_birth = datetime.date(1990, 5, 15)
    response = client.put(f"/hello/{username}", json={"dateOfBirth": str(date_of_birth)})
 
    assert response.status_code == 204
    assert db_session.merge.called
    assert db_session.merge.call_args.args[0].username == username
    assert db_session.merge.call_args.args[0].date_of_birth == date_of_birth
    assert db_session.commit.called
    assert not db_session.rollback.called

def test_create_user_invalid_username(db_session, client):
    username = "test123"  # contains non-alpha
    date_of_birth = datetime.date(1990, 5, 15)
    response = client.put(f"/hello/{username}", json={"dateOfBirth": str(date_of_birth)})
    
    assert not db_session.merge.called
    assert response.status_code == 400
    assert response.json() == {"detail": "Username must contain only letters."}

def test_create_user_future_date_of_birth(client):
    username = "testuser"
    future_date = datetime.date.today() + datetime.timedelta(days=1)
    response = client.put(f"/hello/{username}", json={"dateOfBirth": str(future_date)})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "The date of birth must be a date before the today date"}

def test_create_user_except(db_session, client):
    username = "testuser"
    future_date = datetime.date.today() - datetime.timedelta(days=1)
    db_session.commit.side_effect = IntegrityError(MagicMock(), MagicMock(), MagicMock())
    response = client.put(f"/hello/{username}", json={"dateOfBirth": str(future_date)})

    assert response.status_code == 500
    assert db_session.merge.called
    assert db_session.rollback.called
    assert response.json() == {"detail": "Error inserting or updating user"}

def test_create_user_duplicate_username(client):
    username = "existinguser"
    date_of_birth = datetime.date(1990, 5, 15)
    response = client.put(f"/hello/{username}", json={"dateOfBirth": str(date_of_birth)})
    assert response.status_code == 204
    response = client.put(f"/hello/{username}", json={"dateOfBirth": str(date_of_birth)})
    assert response.status_code == 204
    date_of_birth = datetime.date(1991, 5, 15)
    response = client.put(f"/hello/{username}", json={"dateOfBirth": str(date_of_birth)})
    assert response.status_code == 204

def test_get_user_existing_user(db_session, client):
    username = "testuser"

    query_mock = MagicMock()
    filter_mock = MagicMock()
    user = User(username=username, date_of_birth=datetime.date(1990, 5, 15))
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = user
    db_session.query.return_value = query_mock

    response = client.get(f"/hello/{username}")
    assert response.status_code == 200
    assert "Hello, testuser!" in response.json()["message"]

def test_get_user_bday_today(db_session, client):
    username = "testuser"

    query_mock = MagicMock()
    filter_mock = MagicMock()
    user = User(username=username, date_of_birth=datetime.date.today())
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = user
    db_session.query.return_value = query_mock

    response = client.get(f"/hello/{username}")
    assert response.status_code == 200
    assert f"Hello, {username}! Happy birthday!" == response.json()["message"]

def test_get_user_non_existing_user(db_session, client):
    username = "nonexistentuser"

    query_mock = MagicMock()
    filter_mock = MagicMock()
    query_mock.filter.return_value = filter_mock
    filter_mock.first.return_value = None
    db_session.query.return_value = query_mock

    assert not db_session.merge.called
    assert not db_session.commit.called
    assert not db_session.revert.called
    response = client.get(f"/hello/{username}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}