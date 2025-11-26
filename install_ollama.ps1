# Autonomous Jarvis AI - Installation Script for Ollama
# Run this script to install Ollama and download the required model

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  Autonomous Jarvis AI Setup" -ForegroundColor Cyan
Write-Host "  Installing Ollama and Models" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is already installed
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue

if ($ollamaPath) {
    Write-Host "✅ Ollama is already installed at: $($ollamaPath.Source)" -ForegroundColor Green
}
else {
    Write-Host "📥 Downloading Ollama installer..." -ForegroundColor Yellow
    
    # Download Ollama installer
    $ollamaUrl = "https://ollama.com/download/OllamaSetup.exe"
    $installerPath = "$env:TEMP\OllamaSetup.exe"
    
    try {
        Invoke-WebRequest -Uri $ollamaUrl -OutFile $installerPath
        Write-Host "✅ Download complete" -ForegroundColor Green
        
        # Run installer
        Write-Host "🚀 Running Ollama installer..." -ForegroundColor Yellow
        Write-Host "   Please follow the installation wizard" -ForegroundColor Gray
        Start-Process -FilePath $installerPath -Wait
        
        # Clean up
        Remove-Item $installerPath -ErrorAction SilentlyContinue
        
        Write-Host "✅ Ollama installation complete" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to download Ollama: $_" -ForegroundColor Red
        Write-Host "💡 Please download manually from: https://ollama.com/download" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  Downloading AI Models" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Start Ollama service
Write-Host "🔄 Starting Ollama service..." -ForegroundColor Yellow
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 3

# Download Qwen2.5-Coder model
Write-Host "📦 Pulling Qwen2.5-Coder model (this may take 10-20 minutes)..." -ForegroundColor Yellow
Write-Host "   Model size: ~8-9 GB" -ForegroundColor Gray
Write-Host ""

try {
    & ollama pull qwen2.5-coder:14b-instruct-q4_K_M
    Write-Host ""
    Write-Host "✅ Model downloaded successfully!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to pull model: $_" -ForegroundColor Red
    Write-Host "💡 Try running manually: ollama pull qwen2.5-coder:14b-instruct-q4_K_M" -ForegroundColor Yellow
    exit 1
}

# Optional: Download smaller model for faster testing
Write-Host ""
$downloadSmaller = Read-Host "Would you like to download a smaller, faster model (7B) for testing? (y/n)"

if ($downloadSmaller -eq 'y' -or $downloadSmaller -eq 'Y') {
    Write-Host "📦 Pulling Qwen2.5-Coder 7B model..." -ForegroundColor Yellow
    & ollama pull qwen2.5-coder:7b-instruct
    Write-Host "✅ Smaller model downloaded!" -ForegroundColor Green
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  Verification" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# List installed models
Write-Host "📋 Installed models:" -ForegroundColor Yellow
& ollama list

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Install Python dependencies: pip install -r backend/requirements.txt" -ForegroundColor White
Write-Host "  2. Start the backend: cd backend; python main.py" -ForegroundColor White
Write-Host "  3. Start the frontend: cd frontend; npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Or use the startup script: start_autonomous_jarvis.bat" -ForegroundColor White
Write-Host ""
