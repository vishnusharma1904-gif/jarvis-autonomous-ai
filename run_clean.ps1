# Clean Launch Script for Jarvis AI
# Kills old processes, installs dependencies, and starts fresh

Write-Host "INITIALIZING CLEAN LAUNCH..." -ForegroundColor Cyan

# 1. Kill existing processes
Write-Host "Cleaning up old processes..." -ForegroundColor Yellow
Stop-Process -Name "python" -ErrorAction SilentlyContinue
Stop-Process -Name "node" -ErrorAction SilentlyContinue
Stop-Process -Name "uvicorn" -ErrorAction SilentlyContinue

# 2. Install Backend Requirements
Write-Host "Checking Backend Dependencies..." -ForegroundColor Yellow
cd backend
pip install -r requirements.txt
# Try to install RAG dependencies
pip install sentence-transformers chromadb -ErrorAction SilentlyContinue 

# 3. Install Frontend Requirements
Write-Host "Checking Frontend Dependencies..." -ForegroundColor Yellow
cd ../frontend
npm install

# 4. Start Backend
Write-Host "Starting Backend Server..." -ForegroundColor Green
cd ../backend
Start-Process cmd -ArgumentList "/k python main.py" -WindowStyle Normal

# 5. Start Frontend
Write-Host "Starting Frontend Server..." -ForegroundColor Green
cd ../frontend
Start-Process cmd -ArgumentList "/k npm run dev" -WindowStyle Normal

# 6. Launch Browser
Start-Sleep -Seconds 5
Write-Host "Launching Interface..." -ForegroundColor Cyan
Start-Process "http://localhost:5174"

Write-Host "LAUNCH COMPLETE!" -ForegroundColor Green
Write-Host "Backend running in Window 1"
Write-Host "Frontend running in Window 2"
