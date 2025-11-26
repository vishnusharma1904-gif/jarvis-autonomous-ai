@echo off
echo ====================================
echo   Autonomous Jarvis AI
echo   Starting System...
echo ====================================
echo.

REM Check if Ollama is running
echo Checking Ollama status...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo Starting Ollama service...
    start "Ollama Service" /MIN ollama serve
    timeout /t 5 /nobreak >nul
) else (
    echo Ollama is already running
)

echo.
echo ====================================
echo   Starting Backend Server
echo ====================================
echo.

REM Start backend
cd backend
start "Jarvis Backend" cmd /k "python main.py"
cd ..

echo Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

echo.
echo ====================================
echo   Starting Frontend
echo ====================================
echo.

REM Start frontend
cd frontend
start "Jarvis Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ====================================
echo   Autonomous Jarvis AI Started!
echo ====================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:5174
echo.
echo Press any key to exit (servers will keep running)...
pause >nul
