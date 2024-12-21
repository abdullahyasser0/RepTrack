# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Expose port 80 for Azure Web App compatibility
EXPOSE 80

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies and create a non-root user
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    adduser --disabled-password --gecos "" appuser && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy dependencies first (for Docker layer caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Set environment variables (build arguments passed during Docker build)
ARG SMTP_EMAIL
ARG SMTP_PASSWORD
ARG SUPABASE_KEY
ARG SUPABASE_URL

# Export build arguments as runtime environment variables
ENV ENVIRONMENT=production
ENV SMTP_EMAIL=${SMTP_EMAIL}
ENV SMTP_PASSWORD=${SMTP_PASSWORD}
ENV SUPABASE_KEY=${SUPABASE_KEY}
ENV SUPABASE_URL=${SUPABASE_URL}

# Set user permissions
RUN chown -R appuser /app
USER appuser

# Use Gunicorn to serve the application in production
CMD ["sh", "-c", "python backend/manage.py makemigrations && python backend/manage.py migrate && gunicorn --bind 0.0.0.0:80 backend.wsgi:application"]
#alohaa
