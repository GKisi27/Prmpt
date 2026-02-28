@echo off
echo ========================================
echo Starting Prmpt Local Environment
echo ========================================

echo [1/2] Starting Backend...
start cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

echo [2/2] Starting Frontend...
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Services are starting in new windows.
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:5173
echo ========================================
echo Close those windows to stop the servers.
pause
