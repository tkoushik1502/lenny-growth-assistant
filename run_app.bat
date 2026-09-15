@echo off
echo ========================================================
echo   Starting The Lenny Growth Assistant
echo ========================================================

:: Check Python venv
if not exist "venv\Scripts\python.exe" (
    echo [1/3] Creating Python virtual environment...
    python -m venv venv
    call .\venv\Scripts\activate.bat
    pip install -r requirements.txt
)

:: Check frontend node_modules
if not exist "frontend\node_modules" (
    echo [2/3] Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

echo [3/3] Launching Backend and Frontend...
start "Lenny Backend (Port 8000)" cmd /k "set PYTHONPATH=backend&& .\venv\Scripts\uvicorn.exe app.main:app --port 8000 --host 0.0.0.0 --reload"
start "Lenny Frontend (Port 3000)" cmd /k "cd frontend&& npm run dev -- --host 0.0.0.0"

echo.
echo ========================================================
echo   Lenny Growth Assistant is launching!
echo   - Web Application: http://localhost:3000
echo   - Backend Swagger: http://localhost:8000/docs
echo ========================================================
