# revolut home task

## src folder

Contains the Python source code to serve Hello API.

- API built using FastAPI and Pydantic models
    - FastAPI facilitates the implementatio of APIs with minimal fuss and a quick start up with plenty of examples
    - Pydantic implements type enforcement

- Sqlalchemy for DB handling
    - SqlAlchemy easy the connection with the DB and is pretty well documented.

## migrations folder

The SQL code to initialise and upgrade the DB

## tests folder

Unit tests for the API get/put routes using pytest

```
pytest tests/test_unit.py
```

## Dockerfile

Builds the docker image for Hello API including its Python dependencies

## docker-compose.yaml

**For local testingx**

Starts up a local PostgreSQL server and uvicorn server to serve the API.

```docker-compose up --build```

The API is available in https://localhost:8000

eg:

```
% http GET localhost:8000/hello/userq
HTTP/1.1 404 Not Found
content-length: 27
content-type: application/json
date: Wed, 17 Jul 2024 17:59:09 GMT
server: uvicorn

{
    "detail": "User not found"
}


% http GET localhost:8000/hello/usera
HTTP/1.1 200 OK
content-length: 58
content-type: application/json
date: Wed, 17 Jul 2024 17:59:12 GMT
server: uvicorn

{
    "message": "Hello, usera! Your birthday is in 364 day(s)"
}
```

