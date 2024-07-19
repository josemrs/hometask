# Revolut home task

This documents is about the code and other deployment pieces.

Other interesting documents are CICD.md and TODO.md.

## Hello API Endpoints

**For a nicer and more updated doc check /docs endpoins while running the app**

### PUT `/hello/<username> { “dateOfBirth”: “YYYY-MM-DD” }`

Saves/updates the given user’s name and date of birth in the database.
Response: 204 No Content

### GET `/hello/<username>`
Returns hello birthday message for the given user
Response: 200 OK

### GET `/metrics`
Prometheus metrics

### GET `/docs`
Swagger style docs

## src folder

Contains the Python source code to serve Hello API.

- API built using [FastAPI](https://fastapi.tiangolo.com/) 
    - Facilitates the implementatio of APIs with minimal fuss and a quick start up with plenty of examples
    - Pydantic implements type enforcement
    - Swagger doc "for free"
- [Pydantic](https://docs.pydantic.dev/latest/) models
- [Sqlalchemy](https://www.sqlalchemy.org/) for DB handling
    - SqlAlchemy easy the connection with the DB and is pretty well documented.

- https://github.com/trallnag/prometheus-fastapi-instrumentator

## migrations folder

The SQL code to initialise and upgrade the DB.

FastAPI is capable of initialising the DB with the coded models.

This would be preffered if the DB wants to be populated with **data** in addition to just schemas.

## tests folder

Unit tests for the API get/put routes using pytest

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/test_unit.py
```

## Dockerfile

Builds the docker image for Hello API including its Python dependencies

## docker-compose.yaml

**For local testing**

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

## charts/hometask

**The helm chart is not published due to privacy concerns, GitHub Pages are public even though the repository is private**

**You have to use the local helm chart**

Helm chart to deploy Hello API in K8S. Includes:

  - Deployment
  - Service (ClusterIP)
  - Ingress (To be deployed when an Ingress Controler is available)
  - Secret for GitHub Container Registry access
  - ...

### For local testing on K8S

- Install minikube and run ```minikube start```
- secret.yaml
  - This is required to download the revolut-hometask image pushed to GHCR
  - Requires a Token for josemrs registry
- Spin up a PostgreSQL deployment
  - ```helm install postgresql oci://registry-1.docker.io/bitnamicharts/postgresql```
  - You will get instructions about how to get user and password, write that down.
- Configure PostgreSQL EnvVars in the values.yaml
  - ```DATABASE_HOST```
  - ```DATABASE_USER```
  - ```DATABASE_PASS```
- Create the namespace for Hello API. Update ```.Values.namespace``` if not ```homestask```
- Deploy Hello API: ```helm install hometask ./hometask``` 