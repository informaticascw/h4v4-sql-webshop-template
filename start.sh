#!/bin/bash

echo "🔁 Stopping old server..."

# Stop alle oude servers
pkill -f "python app/main.py" 2>/dev/null

# Wait until the process has stopped
while pgrep -f "python app/main.py" > /dev/null; do
    echo "⏳ Waiting for old server to stop..."
    sleep 1
done

echo "✅ Old server stopped"

echo "📦 Initializing database..."

# Remove the old database file if it exists
rm -f data/products.db

# (Re)create database from init.sql
sqlite3 data/products.db < data/init.sql

echo "✅ Database ready"

echo "🚀 Starting FastAPI backend (using python)..."

# Start FastAPI server via python, vereist uvicorn.run() in main.py
python app/main.py

