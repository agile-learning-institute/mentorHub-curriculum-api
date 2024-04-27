FROM python:3.12

WORKDIR /src/flask_app


# Copy the dependencies file to the working directory
COPY src/flask_app/requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/flsk_app/ .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python3", "main.py"]
