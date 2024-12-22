# Use an official Python runtime as a parent image
FROM python:3.12


# Set environment variables
ENV ENVIRONMENT=production
ENV SMTP_EMAIL=${SMTP_EMAIL}
ENV SMTP_PASSWORD=${SMTP_PASSWORD}
ENV SUPABASE_KEY=${SUPABASE_KEY}
ENV SUPABASE_URL=${SUPABASE_URL} 


ARG SMTP_EMAIL
ARG SMTP_PASSWORD
ARG SUPABASE_KEY
ARG SUPABASE_URL

# Set the working directory in the container
WORKDIR /app/backend

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
# CMD ["python", "back/manage.py", "migrate;", "python", "back/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
# CMD ["sh", "-c","python rehla/manage.py runserver 0.0.0.0:8000"]
