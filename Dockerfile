# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim


# Use an official Python runtime as a parent image
FROM python:3.12


EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


ARG SMTP_EMAIL
ARG SMTP_PASSWORD
ARG SUPABASE_KEY
ARG SUPABASE_URL

# Set environment variables
ENV ENVIRONMENT=production
ENV SMTP_EMAIL=${SMTP_EMAIL}
ENV SMTP_PASSWORD=${SMTP_PASSWORD}
ENV SUPABASE_KEY=${SUPABASE_KEY}
ENV SUPABASE_URL=${SUPABASE_URL}


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "backend.wsgi:application"]
