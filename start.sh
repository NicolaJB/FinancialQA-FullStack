#!/bin/bash

# Activate backend virtual environment
source backend/venv/bin/activate

# Start backend (FastAPI)
echo "Starting FastAPI backend on port 8000..."
uvicorn app.main:app --reload --port 8000 &

# Start frontend (assumes you have a frontend folder and npm project)
echo "Starting frontend..."
cd frontend || exit 1
npm start
