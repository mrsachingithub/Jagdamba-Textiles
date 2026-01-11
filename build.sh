#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
flask db upgrade

# Seed database (Create admin user if missing)
python create_db.py
