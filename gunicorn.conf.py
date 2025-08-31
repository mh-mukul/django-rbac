import os
import multiprocessing

# Derive sane defaults (can be overridden by env or CLI args)
workers = int(os.getenv("GUNICORN_WORKERS", max(
    2, (multiprocessing.cpu_count() or 2))))
threads = int(os.getenv("GUNICORN_THREADS", 2))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gthread")
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", 1000))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", 200))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", 5))
accesslog = os.getenv("GUNICORN_ACCESSLOG", "-")  # stdout
errorlog = os.getenv("GUNICORN_ERRORLOG", "-")    # stderr
loglevel = os.getenv("GUNICORN_LOGLEVEL", "info")
# Ensure temporary files go to a writable location in containers
worker_tmp_dir = "/dev/shm"

# Security: do not reveal server type
raw_env = [
    "DJANGO_SETTINGS_MODULE=" +
    os.getenv("DJANGO_SETTINGS_MODULE", "config.settings"),
]

# Optional: limit request line/fields for DoS protection
limit_request_line = int(os.getenv("GUNICORN_LIMIT_REQUEST_LINE", 4094))
limit_request_fields = int(os.getenv("GUNICORN_LIMIT_REQUEST_FIELDS", 100))
