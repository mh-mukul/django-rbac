#!/usr/bin/env bash
set -euo pipefail

# Colors for logs
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

log() { echo -e "${GREEN}[entrypoint]${NC} $*"; }
warn() { echo -e "${YELLOW}[entrypoint]${NC} $*"; }
err() { echo -e "${RED}[entrypoint]${NC} $*"; }

# Optional: wait for a database if DATABASE is set to postgres or mysql
wait_for_db() {
  if [ "${DB_TYPE:-sqlite}" != "sqlite" ]; then
    warn "Checking DB connectivity before starting..."
    ATTEMPTS=10

    case "${DJANGO_ENV:-prod}" in
      dev) SETTINGS_MODULE="config.settings.dev" ;;
      staging) SETTINGS_MODULE="config.settings.staging" ;;
      prod|*) SETTINGS_MODULE="config.settings.prod" ;;
    esac

    until DJANGO_SETTINGS_MODULE=${SETTINGS_MODULE} \
      python -c "import django; django.setup(); from django.db import connections; connections['default'].cursor()" >/dev/null 2>&1; do
      ATTEMPTS=$((ATTEMPTS-1)) || true
      if [ "$ATTEMPTS" -le 0 ]; then
        err "Database is not reachable. Exiting."; exit 1
      fi
      warn "DB not ready, retrying in 3s... ($ATTEMPTS left)"
      sleep 3
    done
    log "Database reachable."
  else
    log "DB_TYPE is sqlite, skipping DB connectivity check."
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
  log "Starting Gunicorn..."
  exec gunicorn \
    --config gunicorn.conf.py \
    config.wsgi:application
}

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