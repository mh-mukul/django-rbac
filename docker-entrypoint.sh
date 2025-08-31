#!/usr/bin/env bash
set -euo pipefail

# Colors for logs
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

log() { echo -e "${GREEN}[entrypoint]${NC} $*"; }
warn() { echo -e "${YELLOW}[entrypoint]${NC} $*"; }
err() { echo -e "${RED}[entrypoint]${NC} $*"; }

# Default values
: "${DJANGO_SETTINGS_MODULE:=config.settings}"
: "${GUNICORN_BIND:=0.0.0.0:8000}"
: "${GUNICORN_WORKERS:=3}"
: "${GUNICORN_THREADS:=2}"
: "${GUNICORN_TIMEOUT:=60}"

# Optional: wait for a database if DATABASE_URL is set
wait_for_db() {
  if [ -n "${DATABASE_URL:-}" ]; then
    warn "DATABASE_URL detected. Checking DB connectivity before starting..."
    # Try a lightweight Django check to validate DB connection
    ATTEMPTS=3
    until python manage.py check --database default >/dev/null 2>&1; do
      ATTEMPTS=$((ATTEMPTS-1)) || true
      if [ "$ATTEMPTS" -le 0 ]; then
        err "Database is not reachable. Exiting."; exit 1
      fi
      warn "DB not ready, retrying in 3s... ($ATTEMPTS left)"; sleep 3
    done
    log "Database reachable."
  else
    warn "No DATABASE_URL provided; skipping DB wait."
  fi
}

collect_static() {
  if [ "${SKIP_COLLECTSTATIC:-0}" != "1" ]; then
    log "Collecting static files..."
    python manage.py collectstatic --noinput
  else
    warn "Skipping collectstatic (SKIP_COLLECTSTATIC=1)."
  fi
}

run_migrations() {
  if [ "${SKIP_MIGRATIONS:-0}" != "1" ]; then
    log "Applying database migrations..."
    python manage.py migrate --noinput
  else
    warn "Skipping migrations (SKIP_MIGRATIONS=1)."
  fi
}

start_gunicorn() {
  log "Starting Gunicorn on ${GUNICORN_BIND} with ${GUNICORN_WORKERS} workers, ${GUNICORN_THREADS} threads..."
  exec gunicorn \
    --config gunicorn.conf.py \
    --bind "${GUNICORN_BIND}" \
    --workers "${GUNICORN_WORKERS}" \
    --threads "${GUNICORN_THREADS}" \
    --timeout "${GUNICORN_TIMEOUT}" \
    config.wsgi:application
}

# Health endpoint (simple)
export HEALTHCHECK_PATH=${HEALTHCHECK_PATH:-/health/}

# Run lifecycle
wait_for_db
collect_static
run_migrations

# Allow running arbitrary commands e.g. `docker run ... manage.py shell`
if [ "$#" -gt 0 ]; then
  log "Executing custom command: $*"
  exec "$@"
else
  start_gunicorn
fi