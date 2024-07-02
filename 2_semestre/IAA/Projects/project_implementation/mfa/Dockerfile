# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
COPY ./templates /app/templates

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# Run the Python script
CMD ["python", "mfa.py"]
