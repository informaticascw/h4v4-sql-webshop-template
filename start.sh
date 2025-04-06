#!/bin/bash

echo "🔁 Stopping old servers..."

# Stop alle oude servers
pkill -f "python app/main.py" 2>/dev/null

echo "✅ Old processes stopped"

echo "📦 Initializing database..."

# (Re)create database from init.sql
sqlite3 data/products.db < data/init.sql

echo "✅ Database ready"

echo "🚀 Starting FastAPI backend (via python)..."

# Start FastAPI server via python, vereist uvicorn.run() in main.py
python app/main.py &

