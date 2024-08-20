# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /app/

# Install pipenv and dependencies
RUN pip install pipenv && pipenv install --deploy --system

# Install Gunicorn for running the Flask app in production
RUN pipenv install gunicorn

# Verify Gunicorn installation
RUN pipenv run gunicorn --version

# Copy the rest of the application code to the working directory
COPY . /app

# Expose the port the app will run on
EXPOSE 8088

# Command to run the application using Gunicorn
CMD pipenv run gunicorn --bind 0.0.0.0:8088 src.server:app
# CMD ["gunicorn", "--bind", "0.0.0.0:8088", "src.server:app"]