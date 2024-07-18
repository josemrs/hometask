# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory
WORKDIR /hello-api

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./src .

# Expose the port FastAPI is running on
EXPOSE 8000 

ENTRYPOINT uvicorn api:api --host 0.0.0.0 --port 8000