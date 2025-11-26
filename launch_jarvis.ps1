# PowerShell Script to Start Jarvis AI
# This script installs dependencies and starts both servers

Write-Host "🚀 Starting Jarvis AI Setup & Launch..." -ForegroundColor Cyan

# 1. Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found! Please install Python 3.10+" -ForegroundColor Red
    Pause
    Exit
}

# 2. Install Backend Dependencies
Write-Host "📦 Installing Backend Dependencies..." -ForegroundColor Yellow
cd backend
pip install -r requirements.txt
pip install ollama langchain langchain-community langchain-core
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install backend dependencies" -ForegroundColor Red
    Pause
    Exit
}

# 3. Install Frontend Dependencies
Write-Host "📦 Installing Frontend Dependencies..." -ForegroundColor Yellow
cd ../frontend
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install frontend dependencies" -ForegroundColor Red
    Pause
    Exit
}

# 4. Start Servers
Write-Host "✅ Setup Complete! Launching Servers..." -ForegroundColor Green

# Start Backend in new window
cd ../backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python main.py" -WindowStyle Normal
Write-Host "Started Backend Server (Window 1)" -ForegroundColor Cyan

# Start Frontend in new window
cd ../frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal
Write-Host "Started Frontend Server (Window 2)" -ForegroundColor Cyan

# 5. Open Browser
Start-Sleep -Seconds 5
Write-Host "🌐 Opening Browser..." -ForegroundColor Green
Start-Process "http://localhost:5174"

Write-Host "🎉 Jarvis AI is running!" -ForegroundColor Green
Write-Host "If you see errors in the other windows, please check them." -ForegroundColor Gray
Pause
