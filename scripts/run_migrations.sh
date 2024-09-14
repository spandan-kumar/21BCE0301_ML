#!/bin/bash

# Navigate to the project root directory
cd "$(dirname "$0")/.."

# Activate the virtual environment if you're using one
# source venv/bin/activate

# Run Alembic migrations
alembic upgrade head

echo "Migrations completed successfully."
