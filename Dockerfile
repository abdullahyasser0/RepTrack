FROM python:3.12

# Set the working directory
WORKDIR /app
# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000


# Set environment variables (build arguments passed during Docker build)
ARG SMTP_EMAIL
ARG SMTP_PASSWORD
ARG SUPABASE_KEY
ARG SUPABASE_URL

# Export build arguments as runtime environment variables

# Environment variables for the container
ENV SMTP_EMAIL=$SMTP_EMAIL \
    SMTP_PASSWORD=$SMTP_PASSWORD \
    SUPABASE_KEY=$SUPABASE_KEY \
    SUPABASE_URL=$SUPABASE_URL

# Expose ports
EXPOSE 8000

# Set the default command
CMD ["sh", "-c", "python backend/manage.py makemigrations && python backend/manage.py migrate && python backend/manage.py runserver 0.0.0.0:8000"]
