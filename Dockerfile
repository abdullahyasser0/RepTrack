FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .
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

# Expose ports
EXPOSE 8000

# Set the default command
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
