#!/bin/bash

echo "Starting frontend and backend..."

# Start backend
cd backend
uvicorn app:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Print status
echo "Backend running at http://localhost:8000"
echo "Frontend running at http://localhost:5173 or http://localhost:3000"

# Wait for both
wait $BACKEND_PID
wait $FRONTEND_PID
