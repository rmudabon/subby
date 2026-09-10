#!/bin/sh
# Exit immediately when migrations or application startup fails.
set -e

echo "Running database migrations..."
uv run alembic upgrade head

echo "Starting FastAPI application..."
exec "$@"
