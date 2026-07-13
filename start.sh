#!/bin/bash

# Start Docker containers in the background
echo "Starting Docker services (PostgreSQL, Redis, Qdrant, Neo4j)..."
docker compose up -d

# Check if the python environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Error: Virtual environment 'venv' not found! Please set up the environment first."
    exit 1
fi

# Start the FastAPI application
echo "Starting FastAPI server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
