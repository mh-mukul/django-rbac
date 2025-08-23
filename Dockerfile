FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV=prod
ENV DJANGO_SETTINGS_MODULE=config.settings

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir -r requirements/prod.txt

# Copy the project
COPY . /app/

# Make the scripts executable
RUN chmod +x /app/scripts/*.sh

# Collect static files
RUN python manage.py collectstatic --no-input

# Run the entrypoint script
ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# Default command
CMD ["gunicorn"]

# Expose the port
EXPOSE 8000
