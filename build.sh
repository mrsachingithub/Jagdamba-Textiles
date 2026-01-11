#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
flask db upgrade

# Seed database (optional, only if needed and safe)
# python seed_data.py
