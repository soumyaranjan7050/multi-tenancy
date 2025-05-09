# Dockerfile

# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files (optional)
RUN python manage.py collectstatic --noinput

# Expose the default port
EXPOSE 8000

# Run migrations and start the app
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
