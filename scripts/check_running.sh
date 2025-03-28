#!/bin/bash

# Configuration
LOG_DIR="/var/www-tools/contapp/logs"
CONFIG_DIR="/var/www-tools/contapp/config"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Check if gunicorn is running for the app
if pgrep -f "gunicorn.*contapp.*wsgi:application" > /dev/null; then
    # Already running
    exit 0
fi

# Make sure directories exist
mkdir -p "$LOG_DIR"

# Start ContApp with Gunicorn
cd /var/www-tools/contapp
source /var/www-tools/contapp/venv/bin/activate

/var/www-tools/contapp/venv/bin/gunicorn \
    --bind 0.0.0.0:8086 \
    --workers 2 \
    --timeout 120 \
    --access-logfile "$LOG_DIR/access.log" \
    --error-logfile "$LOG_DIR/error.log" \
    --log-level info \
    wsgi:application >> "$LOG_DIR/contapp.log" 2>&1 &

deactivate
