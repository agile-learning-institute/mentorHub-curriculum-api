# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /app/

# Install pipenv and dependencies
RUN pip install pipenv && pipenv install --deploy --system

# Install Gunicorn for running the Flask app in production
RUN pip install gunicorn

# Copy the rest of the application code to the working directory
COPY . /app

# Expose the port the app will run on
EXPOSE 8088

# Set Environment Variables
ENV PYTHONPATH=/app

# Command to run the application using Gunicorn with debug logging
CMD gunicorn -c gunicorn.conf.py --chdir /app --pythonpath /app --log-level debug --bind 0.0.0.0:8088 src.server:app
