# Multi-stage Dockerfile for a Django application with Gunicorn and Tini
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install build deps (for compiling wheels)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt ./
# Install to a temp location we can copy from (keeps final image smaller)
RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# Final stage: minimal runtime image
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    # Gunicorn sensible defaults (override via env)
    GUNICORN_WORKERS=3 \
    GUNICORN_THREADS=2 \
    GUNICORN_TIMEOUT=60 \
    GUNICORN_BIND=0.0.0.0:8000

# Minimal runtime libs for common Python deps (psycopg, Pillow, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    zlib1g \
    tini \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed site-packages from builder image
COPY --from=builder /install /usr/local

# Set workdir
WORKDIR /app

# Copy project code
COPY . .

# Ensure entrypoint is executable
RUN chmod +x /app/docker-entrypoint.sh

# Direct logs to stdout/stderr
ENV DJANGO_LOG_LEVEL=info

# Expose Gunicorn port
EXPOSE 8000

# Use Tini as init to handle PID 1 properly
ENTRYPOINT ["/usr/bin/tini", "--", "/app/docker-entrypoint.sh"]