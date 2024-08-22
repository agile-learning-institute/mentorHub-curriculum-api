# Stage 1: Build stage
FROM python:3.12-slim as build

# Install Git and other dependencies
RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

# Copy the entire context to the container
COPY . .

# Get the current Git branch and build time
RUN BRANCH=$(git rev-parse --abbrev-ref HEAD) && \
    DATE=$(date +'%Y%m%d-%H%M%S') && \
    echo "${BRANCH}-${DATE}" > /app/BUILT_AT

# Stage 2: Production stage
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /opt/mentorhub-curriculum-api

# Copy the entire source code and the BUILT_AT file from the build stage
COPY --from=build /app/ /opt/mentorhub-curriculum-api/

# Install pipenv and dependencies
COPY Pipfile Pipfile.lock /opt/mentorhub-curriculum-api/
RUN pip install pipenv && pipenv install --deploy --system

# Install Gunicorn for running the Flask app in production
RUN pip install gunicorn gevent

# Expose the port the app will run on
EXPOSE 8088

# Set Environment Variables
ENV PYTHONPATH=/opt/mentorhub-curriculum-api

# Command to run the application using Gunicorn with exec to forward signals
CMD exec gunicorn --bind 0.0.0.0:8088 src.server:app
